from neomodel.exceptions import UniqueProperty
from ..sources import collect_sources
from . import Person, SourceConcept, Subject, Work, get_logger
from .decorators import handle_neo4j_session_timeout

log = get_logger(__name__)


@handle_neo4j_session_timeout
def ingest_work(work_data):
    """
    Add a new work node to the graph.
    """
    log.info("Processing work", work_id=work_data["_id"])
    try:
        production_date = work_data["production"][0]["dates"][0]["label"]
    except (KeyError, IndexError, TypeError):
        production_date = None

    try:
        work = Work(
            type="work",
            wellcome_id=work_data["_id"],
            title=work_data["title"],
            format=work_data["format"]["label"],
            published=production_date,
        ).save()
    except UniqueProperty:
        return

    for contributor in work_data["contributors"]:
        try:
            if "sourceIdentifier" in contributor["agent"]["id"]:
                source_identifier = contributor["agent"]["id"]["sourceIdentifier"]
                source_id = source_identifier["value"]
                source_type = source_identifier["identifierType"]["id"]
                existing_source_concept = SourceConcept.nodes.first_or_none(
                    source_id=source_id,
                    source_type=source_type,
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
                        label=contributor["agent"]["label"],
                        source_id=source_id,
                    )
                    person = Person(label=contributor["agent"]["label"]).save()
                    collect_sources(
                        target_concept=person,
                        source_id=source_id,
                        source_type=source_type,
                    )
            else:
                log.debug(
                    "Contributor has no source identifier",
                    contributor=contributor["agent"]["label"],
                )
                existing_person = Person.nodes.first_or_none(
                    label=contributor["agent"]["label"]
                )
                if existing_person:
                    person = existing_person
                else:
                    person = Person(label=contributor["agent"]["label"]).save()

                person.contributions.connect(work)
        except Exception as error:
            log.exception(
                "Error connecting contributor to work",
                contributor=contributor,
                work=work.title,
                error=error,
            )

    for work_subject in work_data["subjects"]:
        for work_concept in work_subject["concepts"]:
            wellcome_id = (
                work_concept["id"]["canonicalId"]
                if "canonicalId" in work_concept["id"]
                else None
            )
            try:
                source_identifier = work_concept["id"]["sourceIdentifier"]
            except KeyError:
                log.debug(
                    "Subject has no source identifier",
                    concept=work_concept["label"],
                )
                existing_subject = Subject.nodes.first_or_none(
                    label=work_concept["label"], wellcome_id=wellcome_id, 
                    wellcome_parent_id=work_subject["id"], 
                    wellcome_parent_label=work_subject["label"]
                )
                if existing_subject:
                    subject = existing_subject
                else:
                    subject = Subject(
                        label=work_concept["label"], wellcome_id=wellcome_id,
                        wellcome_parent_id=work_subject["id"], 
                        wellcome_parent_label=work_subject["label"]
                    ).save()
            else:
                source_id = source_identifier["value"]
                source_type = source_identifier["identifierType"]["id"]
                try:
                    existing_subject_source_concept = (
                        SourceConcept.nodes.first_or_none(
                            source_id=source_id, source_type=source_type
                        )
                    )
                except ValueError as error:
                    log.exception(
                        "Error finding source concept",
                        source_id=source_id,
                        source_type=source_type,
                        error=error,
                    )
                    existing_subject_source_concept = None
                if existing_subject_source_concept:
                    log.debug(
                        "Found existing source concept",
                        source_id=existing_subject_source_concept.source_id,
                    )
                    subject = existing_subject_source_concept.parent.all()[0]
                else:
                    log.debug("Creating concept", label=work_concept["label"])

                    subject = Subject.nodes.first_or_none(
                        wellcome_id=wellcome_id
                    )
                    if not subject:
                        subject = Subject(
                            label=work_concept["label"],
                            wellcome_id=wellcome_id,
                            wellcome_parent_id=work_subject["id"], 
                            wellcome_parent_label=work_subject["label"]
                        ).save()

                    collect_sources(
                        target_concept=subject,
                        source_id=source_id,
                        source_type=source_type,
                    )
            try:
                work.concepts.connect(subject)
            except Exception as error:
                log.exception(
                    "Error connecting concept to work",
                    concept=subject.label,
                    work=work.title,
                    error=error,
                )
