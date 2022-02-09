import datetime
from pathlib import Path

import pandas as pd

from src.elasticsearch import yield_popular_works
from src.enrich.wikidata import (
    get_contributor_wikidata_ids,
    get_wikidata,
    get_wikidata_description,
    get_wikidata_id,
    get_wikidata_preferred_name,
    get_wikidata_variant_names,
)
from src.graph import get_neo4j_session
from src.graph.models import Concept, SourceConcept, Work
from src.utils import clean, clean_csv, get_logger

log = get_logger(__name__)

db = get_neo4j_session()

log.info("Loading stories dataset")
df = pd.read_excel(
    pd.ExcelFile("/data/stories/stories.xlsx", engine="openpyxl"),
    sheet_name="Articles",
    dtype={"Date published": datetime.datetime},
).fillna("")


# stories
log.info("Processing stories")
for _, story_data in df.iterrows():
    story_id = Path(story_data["URL"]).name
    log.info("Processing story", story_id=story_id)
    story = Work(
        type="story",
        wellcome_id=story_id,
        title=story_data["Title"],
        published=story_data["Date published"].date(),
        wikidata_id=story_data["Wikidata ID"],
    ).save()

    story_wikidata = get_wikidata(story.wikidata_id)
    contributor_wikidata_ids = get_contributor_wikidata_ids(story_wikidata)
    for contributor_wikidata_id in contributor_wikidata_ids:
        existing_person_source_concept = SourceConcept.nodes.get_or_none(
            source_id=contributor_wikidata_id
        )
        if existing_person_source_concept:
            log.debug(
                "Found existing person source concept",
                wikidata_id=contributor_wikidata_id,
            )
            person = existing_person_source_concept.parent.all()[0]
        else:
            contributor_wikidata = get_wikidata(contributor_wikidata_id)
            source_concept = SourceConcept(
                source_id=contributor_wikidata_id,
                source_type="wikidata",
                description=get_wikidata_description(contributor_wikidata),
                preferred_name=get_wikidata_preferred_name(
                    contributor_wikidata
                ),
                variant_names=get_wikidata_variant_names(contributor_wikidata),
            ).save()
            log.debug("Creating person", name=source_concept.preferred_name)
            person = Concept(
                name=source_concept.preferred_name, type="person"
            ).save()
            person.sources.connect(source_concept)
        story.contributors.connect(person)

    for concept_name in clean_csv(story_data["Keywords"]):
        clean_concept_name = clean(concept_name)
        concept_wikidata_id = get_wikidata_id(clean_concept_name)
        if concept_wikidata_id:
            existing_concept_source_concept = SourceConcept.nodes.get_or_none(
                source_id=concept_wikidata_id
            )
            if existing_concept_source_concept:
                log.debug(
                    "Found existing source concept",
                    wikidata_id=concept_wikidata_id,
                )
                concept = existing_concept_source_concept.parent.all()[0]
            else:
                log.debug("Creating concept", name=clean_concept_name)
                concept = Concept(name=clean_concept_name).save()
                concept.collect_sources(
                    source_id=concept_wikidata_id, source_type="wikidata"
                )
        else:
            concept = Concept.nodes.first_or_none(name=clean_concept_name)
            if not concept:
                concept = Concept(name=clean_concept_name).save()
        story.concepts.connect(concept)


# works
log.info("Processing works")
for document in yield_popular_works(size=10_000):
    try:
        work_data = document["_source"]["data"]
    except KeyError as e:
        log.error("No data found in document", error=e)
        continue
    log.info("Processing work", work_id=document["_id"])
    work = Work(
        wellcome_id=document["_id"], title=work_data["title"], type="work"
    ).save()

    for contributor in work_data["contributors"]:
        try:
            source_identifier = contributor["agent"]["id"]["sourceIdentifier"]
        except KeyError:
            clean_name = clean(contributor["agent"]["label"])
            log.debug(
                "Contributor has no source identifier",
                contributor=clean_name,
            )
            existing_person = Concept.nodes.first_or_none(
                name=clean_name, type="person"
            )
            if existing_person:
                person = existing_person
            else:
                person = Concept(name=clean_name, type="person").save()
        else:
            source_id = source_identifier["value"]
            source_type = source_identifier["identifierType"]["id"]
            try:
                existing_source_concept = SourceConcept.nodes.first_or_none(
                    source_id=source_id,
                    source_type=source_type,
                )
            except ValueError as e:
                log.exception(
                    "Error finding source concept",
                    source_id=source_id,
                    source_type=source_type,
                    error=e,
                )

            if existing_source_concept:
                log.debug(
                    "Found existing person source concept",
                    source_id=existing_source_concept.source_id,
                )
                person = existing_source_concept.parent.all()[0]
            else:
                log.debug(
                    "Creating new person",
                    name=contributor["agent"]["label"],
                    source_id=source_id,
                )
                person = Concept(
                    name=clean(contributor["agent"]["label"]), type="person"
                ).save()
                person.collect_sources(
                    source_id=source_id,
                    source_type=source_type,
                )
        try:
            work.contributors.connect(person)
        except Exception as e:
            log.exception(
                "Error connecting contributor to work",
                contributor=person.name,
                work=work.title,
                error=e,
            )

    for concept in work_data["subjects"]:
        try:
            source_identifier = concept["id"]["sourceIdentifier"]
        except KeyError:
            clean_name = clean(concept["label"])
            log.debug("Concept has no source identifier", concept=clean_name)
            existing_concept = Concept.nodes.first_or_none(name=clean_name)
            if existing_concept:
                concept = existing_concept
            else:
                concept = Concept(name=clean_name).save()
        else:
            source_id = source_identifier["value"]
            source_type = source_identifier["identifierType"]["id"]
            try:
                existing_concept_source_concept = (
                    SourceConcept.nodes.first_or_none(
                        source_id=source_id, source_type=source_type
                    )
                )
            except ValueError as e:
                log.exception(
                    "Error finding source concept",
                    source_id=source_id,
                    source_type=source_type,
                    error=e,
                )
            if existing_concept_source_concept:
                log.debug(
                    "Found existing source concept",
                    source_id=existing_concept_source_concept.source_id,
                )
                concept = existing_concept_source_concept.parent.all()[0]
            else:
                clean_concept_name = clean(concept["label"])
                log.debug("Creating concept", name=clean_concept_name)
                concept = Concept(name=clean_concept_name).save()
                concept.collect_sources(
                    source_id=source_id, source_type=source_type
                )
        try:
            work.concepts.connect(concept)
        except Exception as e:
            log.exception(
                "Error connecting concept to work",
                concept=concept.name,
                work=work.title,
                error=e,
            )
