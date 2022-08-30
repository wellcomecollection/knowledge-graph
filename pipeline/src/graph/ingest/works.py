from . import Concept, SourceConcept, Work, get_logger

log = get_logger(__name__)


def ingest_work(work_data):
    """
    Add a new work node to the graph.
    """
    log.info("Processing work", work_id=work_data["_id"])

    try:
        production_date = work_data["production"][0]["dates"][0]["label"]
    except (KeyError, IndexError, TypeError):
        production_date = None

    work = Work(
        type="work",
        wellcome_id=work_data["_id"],
        title=work_data["title"],
        format=work_data["format"]["label"],
        published=production_date,
    ).save()

    for contributor in work_data["contributors"]:
        wellcome_id = (
            contributor["agent"]["id"]["canonicalId"]
            if "canonicalId" in contributor["agent"]["id"]
            else None
        )
        try:
            source_identifier = contributor["agent"]["id"]["sourceIdentifier"]
        except KeyError:
            log.debug(
                "Contributor has no source identifier",
                contributor=contributor["agent"]["label"],
            )
            existing_person = Concept.nodes.first_or_none(
                label=contributor["agent"]["label"],
                type="person",
                wellcome_id=wellcome_id,
            )
            if existing_person:
                person = existing_person
            else:
                person = Concept(
                    label=contributor["agent"]["label"],
                    type="person",
                    wellcome_id=wellcome_id,
                ).save()
        else:
            source_id = source_identifier["value"]
            source_type = source_identifier["identifierType"]["id"]
            try:
                existing_source_concept = SourceConcept.nodes.first_or_none(
                    source_id=source_id,
                    source_type=source_type,
                )
            except ValueError as error:
                log.exception(
                    "Error finding source concept",
                    source_id=source_id,
                    source_type=source_type,
                    error=error,
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
                person = Concept(
                    label=contributor["agent"]["label"],
                    type="person",
                    wellcome_id=wellcome_id,
                ).save()
                person.collect_sources(
                    source_id=source_id,
                    source_type=source_type,
                )
        try:
            work.contributors.connect(person)
        except Exception as error:
            log.exception(
                "Error connecting contributor to work",
                contributor=person.label,
                work=work.title,
                error=error,
            )

    for subject in work_data["subjects"]:
        for concept in subject["concepts"]:
            wellcome_id = (
                concept["id"]["canonicalId"]
                if "canonicalId" in concept["id"]
                else None
            )
            try:
                source_identifier = concept["id"]["sourceIdentifier"]
            except KeyError:
                log.debug(
                    "Concept has no source identifier", concept=concept["label"]
                )
                existing_concept = Concept.nodes.first_or_none(
                    label=concept["label"], wellcome_id=wellcome_id
                )
                if existing_concept:
                    concept = existing_concept
                else:
                    concept = Concept(
                        label=concept["label"], wellcome_id=wellcome_id
                    ).save()
            else:
                source_id = source_identifier["value"]
                source_type = source_identifier["identifierType"]["id"]
                try:
                    existing_concept_source_concept = (
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
                    existing_concept_source_concept = None
                if existing_concept_source_concept:
                    log.debug(
                        "Found existing source concept",
                        source_id=existing_concept_source_concept.source_id,
                    )
                    concept = existing_concept_source_concept.parent.all()[0]
                else:
                    log.debug("Creating concept", label=concept["label"])
                    concept = Concept(
                        label=concept["label"],
                        wellcome_id=wellcome_id,
                    ).save()
                    concept.collect_sources(
                        source_id=source_id, source_type=source_type
                    )
            try:
                work.concepts.connect(concept)
            except Exception as error:
                log.exception(
                    "Error connecting concept to work",
                    concept=concept.label,
                    work=work.title,
                    error=error,
                )
