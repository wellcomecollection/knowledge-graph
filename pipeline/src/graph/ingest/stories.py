from pathlib import Path

from dateutil.parser import parse

from .. import (
    clean,
    clean_csv,
    get_contributor_wikidata_ids,
    get_wikidata,
    get_wikidata_description,
    get_wikidata_id,
    get_wikidata_preferred_label,
    get_wikidata_variant_labels,
)
from . import Concept, SourceConcept, Work, get_logger

log = get_logger(__name__)


def ingest_story(story_data):
    """
    Add a new story node to the graph.
    """
    try:
        log.info("Processing story", title=story_data["Title"])
        story = Work(
            type="story",
            wellcome_id=Path(story_data["URL"]).name,
            title=story_data["Title"],
            published=story_data["Date published"].date(),
            wikidata_id=story_data["Wikidata ID"],
        ).save()

        if story.wikidata_id:
            story_wikidata = get_wikidata(story.wikidata_id)
            contributor_wikidata_ids = get_contributor_wikidata_ids(
                story_wikidata
            )

            for contributor_wikidata_id in contributor_wikidata_ids:
                existing_person_source_concept = (
                    SourceConcept.nodes.get_or_none(
                        source_id=contributor_wikidata_id
                    )
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
                        description=get_wikidata_description(
                            contributor_wikidata
                        ),
                        preferred_label=get_wikidata_preferred_label(
                            contributor_wikidata
                        ),
                        variant_labels=get_wikidata_variant_labels(
                            contributor_wikidata
                        ),
                    ).save()
                    log.debug(
                        "Creating person", label=source_concept.preferred_label
                    )
                    person = Concept(
                        label=source_concept.preferred_label, type="person"
                    ).save()
                    person.sources.connect(source_concept)
                story.contributors.connect(person)
        else:
            contributors = story_data["Author"].split(",") + story_data[
                "Images by"
            ].split(",")
            for contributor in contributors:
                existing_person_source_concept = (
                    SourceConcept.nodes.get_or_none(preferred_label=contributor)
                )
                if existing_person_source_concept:
                    log.debug(
                        "Found existing person source concept",
                        source_id=existing_person_source_concept.source_id,
                    )
                    person = existing_person_source_concept.parent.all()[0]
                else:
                    log.debug("Creating person", label=contributor)
                    person = Concept(label=contributor, type="person").save()
                story.contributors.connect(person)

        for concept_label in clean_csv(story_data["Keywords"]):
            clean_concept_label = clean(concept_label)
            concept_wikidata_id = get_wikidata_id(clean_concept_label)
            if concept_wikidata_id:
                existing_concept_source_concept = (
                    SourceConcept.nodes.get_or_none(
                        source_id=concept_wikidata_id
                    )
                )
                if existing_concept_source_concept:
                    log.debug(
                        "Found existing source concept",
                        wikidata_id=concept_wikidata_id,
                    )
                    concept = existing_concept_source_concept.parent.all()[0]
                else:
                    log.debug("Creating concept", label=clean_concept_label)
                    concept = Concept(label=clean_concept_label).save()
                    concept.collect_sources(
                        source_id=concept_wikidata_id, source_type="wikidata"
                    )
            else:
                concept = Concept.nodes.first_or_none(label=clean_concept_label)
                if not concept:
                    concept = Concept(label=clean_concept_label).save()
            story.concepts.connect(concept)
    except Exception as error:
        log.exception(
            "Error processing story", title=story_data["Title"], error=error
        )
