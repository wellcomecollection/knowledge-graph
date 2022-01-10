import datetime
from pathlib import Path

import pandas as pd
from structlog import get_logger

from src.enrich.wikidata import (
    get_contributor_wikidata_ids,
    get_wikidata,
    get_wikidata_description,
    get_wikidata_id,
    get_wikidata_preferred_name,
    get_wikidata_variant_names,
)
from src.graph import get_neo4j_session
from src.graph.models import Concept, Person, SourceConcept, Story
from src.utils import clean, clean_csv

log = get_logger()

log.info("Loading stories dataset")
df = pd.read_excel(
    pd.ExcelFile("/data/stories.xlsx", engine="openpyxl"),
    sheet_name="Articles",
    dtype={"Date published": datetime.datetime},
).fillna("")


log.info("Connecting to neo4j")
db = get_neo4j_session()


log.info("Processing stories")
for _, story_data in df.iterrows():
    story_id = Path(story_data["URL"]).name
    log.info("Processing story", story_id=story_id)
    story = Story(
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
                source="wikidata",
                description=get_wikidata_description(contributor_wikidata),
                preferred_name=get_wikidata_preferred_name(
                    contributor_wikidata
                ),
                variant_names=get_wikidata_variant_names(contributor_wikidata),
            ).save()
            log.debug("Creating person", name=source_concept.preferred_name)
            person = Person(name=source_concept.preferred_name).save()
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
                concept.collect_sources(wikidata_id=concept_wikidata_id)
        else:
            concept = Concept.nodes.first_or_none(name=clean_concept_name)
            if not concept:
                concept = Concept(name=clean_concept_name).save()
        story.concepts.connect(concept)

log.info("Getting second order concepts and connections")
for concept in Concept.nodes.all():
    concept.get_neighbours()
