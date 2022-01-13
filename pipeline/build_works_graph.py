import os

from structlog import get_logger

from src.elasticsearch import yield_all_documents
from src.enrich.wikidata import get_wikidata_id
from src.graph import get_neo4j_session
from src.graph.models import Concept, Person, SourceConcept, Work
from src.utils import clean

log = get_logger()

log.info("Loading works dataset")

log.info("Connecting to neo4j")
db = get_neo4j_session()

log.info("Processing works")

works_generator = yield_all_documents(
    index_name=os.environ["ELASTIC_PIPELINE_WORKS_INDEX"],
    host=os.environ["ELASTIC_PIPELINE_HOST"],
    username=os.environ["ELASTIC_PIPELINE_USERNAME"],
    password=os.environ["ELASTIC_PIPELINE_PASSWORD"],
)

for document in works_generator:
    if document["_source"]["type"] != "Visible":
        log.info(
            "Skipping work",
            work_id=document["_id"],
            work_type=document["_source"]["type"],
        )
    else:
        work_data = document["_source"]["data"]
        log.info("Processing work", work_id=document["_id"])
        work = Work(
            wellcome_id=document["_id"], title=work_data["title"]
        ).save()

        for contributor in work_data["contributors"]:
            try:
                source_identifier = contributor["agent"]["id"][
                    "sourceIdentifier"
                ]
            except KeyError:
                clean_name = clean(contributor["agent"]["label"])
                log.debug(
                    "Contributor has no source identifier",
                    contributor=clean_name,
                )
                existing_person = Person.nodes.first_or_none(name=clean_name)
                if existing_person:
                    person = existing_person
                else:
                    person = Person(name=clean_name).save()
            else:
                try:
                    existing_source_concept = SourceConcept.nodes.first_or_none(
                        source_id=source_identifier["value"],
                        source_type=source_identifier["identifierType"]["id"],
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
                        source_id=source_identifier["value"],
                    )
                    person = Person(
                        name=clean(contributor["agent"]["label"])
                    ).save()
                    person.collect_sources(
                        source_id=source_identifier["value"],
                        source_type=source_identifier["identifierType"]["id"],
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

        for concept in work_data["subjects"]:  # + work_data["genres"]:
            try:
                source_identifier = concept["id"]["sourceIdentifier"]
            except KeyError:
                clean_name = clean(concept["label"])
                log.debug(
                    "Concept has no source identifier", concept=clean_name
                )
                existing_concept = Concept.nodes.first_or_none(name=clean_name)
                if existing_concept:
                    concept = existing_concept
                else:
                    concept = Concept(name=clean_name).save()
            else:
                source_id = source_identifier["value"]
                source_type = source_identifier["identifierType"]["id"]
                try:
                    existing_concept_source_concept = SourceConcept.nodes.first_or_none(
                        source_id=source_id, source_type=source_type
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


log.info("Getting second order concepts and connections")
for concept in Concept.nodes.all():
    concept.get_neighbours()
