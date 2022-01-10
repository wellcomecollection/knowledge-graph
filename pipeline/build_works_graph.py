import json

from structlog import get_logger

from src.enrich.wikidata import get_wikidata_id
from src.graph import get_neo4j_session
from src.graph.models import Concept, Person, SourceConcept, Work
from src.utils import clean

log = get_logger()

log.info("Loading works dataset")

log.info("Connecting to neo4j")
db = get_neo4j_session()

log.info("Processing works")
for row in open("/data/works.json", "r"):
    work_data = json.loads(row)
    log.info("Processing work", work_id=work_data["id"])
    work = Work(wellcome_id=work_data["id"], title=work_data["title"]).save()

    for contributor in work_data['contributors']:
        existing_person = Person.nodes.get_or_none(
            name=contributor['agent']['label'],
        )
        if existing_person:
            log.debug(
                "Found existing person", name=contributor['agent']['label'],
            )
            person = existing_person
        else:
            log.debug(
                "Creating new person", name=contributor['agent']['label']
            )
            person = Person(name=contributor['agent']['label']).save()
        work.contributors.connect(person)

    concepts = [
        concept['label']
        for item in work_data["subjects"] + work_data["genres"]
        for concept in item['concepts']
    ]
    for concept_name in concepts:
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
        work.concepts.connect(concept)

# log.info("Getting second order concepts and connections")
# for concept in Concept.nodes.all():
#     concept.get_neighbours()


