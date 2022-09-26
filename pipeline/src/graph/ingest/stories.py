from pathlib import Path

from .. import (
    clean,
    clean_csv,
    get_contributor_wikidata_ids,
    get_wikidata,
    get_wikidata_description,
    search_wikidata,
    get_wikidata_preferred_label,
    get_wikidata_variant_labels,
)
from ..sources import collect_sources
from . import Person, SourceConcept, Subject, Work, get_logger
from .decorators import handle_neo4j_session_timeout

log = get_logger(__name__)


@handle_neo4j_session_timeout
def ingest_story(story_data):
    """
    Add a new story node to the graph.
    """
    try:
        log.info(f'Processing story title: "{story_data["Title"]}"')
        work = Work(
            type="story",
            wellcome_id=Path(story_data["URL"]).name,
            title=story_data["Title"],
            published=story_data["Date published"].date(),
            wikidata_id=story_data["Wikidata ID"],
        ).save()

        if work.wikidata_id:
            work_wikidata = get_wikidata(work.wikidata_id)
            contributor_wikidata_ids = get_contributor_wikidata_ids(
                work_wikidata
            )

            for contributor_wikidata_id in contributor_wikidata_ids:
                contributor = get_or_create_person(
                    work=work,
                    person_wikidata_id=contributor_wikidata_id,
                )
                work.contributors.connect(contributor)

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
                        "Found existing person source concept. "
                        f"source_id: {existing_person_source_concept.source_id}"
                    )
                    person = existing_person_source_concept.parent.all()[0]
                else:
                    log.debug("Creating person", label=contributor)
                    person = Person(label=contributor).save()
                work.contributors.connect(person)

        for subject_label in clean_csv(story_data["Keywords"]):
            clean_subject_label = clean(subject_label)
            subject_wikidata_id = search_wikidata(clean_subject_label)
            if subject_wikidata_id:
                existing_subject_source_concept = (
                    SourceConcept.nodes.get_or_none(
                        source_id=subject_wikidata_id
                    )
                )
                if existing_subject_source_concept:
                    log.debug(
                        "Found existing source concept. "
                        f"wikidata_id: {subject_wikidata_id}",
                    )
                    subject = existing_subject_source_concept.parent.all()[0]
                else:
                    log.debug(f"Creating subject. label: {clean_subject_label}")
                    subject = Subject(label=clean_subject_label).save()
                    collect_sources(
                        target_concept=subject,
                        source_id=subject_wikidata_id,
                        source_type="wikidata",
                    )
            else:
                subject = Subject.nodes.first_or_none(label=clean_subject_label)
                if not subject:
                    subject = Subject(label=clean_subject_label).save()
            work.concepts.connect(subject)
    except Exception as error:
        log.exception(
            "Error processing story. "
            f'title: "{story_data["Title"]}" '
            f'error: "{error}"'
        )


def get_or_create_person(work: Work, person_wikidata_id: str = None):
    existing_person_source_concept = SourceConcept.nodes.get_or_none(
        source_id=person_wikidata_id
    )
    if existing_person_source_concept:
        log.debug(
            "Found existing preson source concept. "
            f"wikidata_id: {person_wikidata_id}",
        )
        person = existing_person_source_concept.parent.all()[0]
    else:
        person_wikidata = get_wikidata(person_wikidata_id)
        source_concept = SourceConcept(
            source_id=person_wikidata_id,
            source_type="wikidata",
            description=get_wikidata_description(person_wikidata),
            preferred_label=get_wikidata_preferred_label(person_wikidata),
            variant_labels=get_wikidata_variant_labels(person_wikidata),
        ).save()
        log.debug(f"Creating person. label: {source_concept.preferred_label}")
        person = Person(
            label=source_concept.preferred_label, type="person"
        ).save()
        person.sources.connect(source_concept)

    return person
