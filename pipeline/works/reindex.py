import json
import os

from elasticsearch import Elasticsearch
from structlog import get_logger

from src.elasticsearch import (
    format_concept_for_elasticsearch,
    format_person_for_elasticsearch,
    format_work_for_elasticsearch,
)
from src.graph import get_neo4j_session
from src.graph.models import Concept, Person, Work

log = get_logger()

db = get_neo4j_session(clear=False)

es = Elasticsearch(
    os.environ["ELASTIC_CONCEPTS_HOST"],
    http_auth=(
        os.environ["ELASTIC_CONCEPTS_USERNAME"],
        os.environ["ELASTIC_CONCEPTS_PASSWORD"],
    ),
)


works_index_name = os.environ["ELASTIC_WORKS_INDEX"]
log.info(f"Creating the works index: {works_index_name}")
with open("/data/elastic/works/mapping.json", "r") as f:
    works_mappings = json.load(f)
with open("/data/elastic/works/settings.json", "r") as f:
    works_settings = json.load(f)

es.indices.delete(index=works_index_name, ignore=404)
es.indices.create(
    index=works_index_name,
    mappings=works_mappings,
    settings=works_settings,
)

log.info("Populating the works index")
for work in Work.nodes.all():
    log.info("Indexing work", work=work.wellcome_id)
    es.index(
        index=works_index_name,
        id=work.wellcome_id,
        document=format_work_for_elasticsearch(work),
    )


concepts_index_name = os.environ["ELASTIC_CONCEPTS_INDEX"]
log.info(f"Creating the concepts index: {concepts_index_name}")
with open("/data/elastic/concepts/mapping.json", "r") as f:
    concepts_mappings = json.load(f)
with open("/data/elastic/concepts/settings.json", "r") as f:
    concepts_settings = json.load(f)

es.indices.delete(index=concepts_index_name, ignore=404)
es.indices.create(
    index=concepts_index_name,
    mappings=concepts_mappings,
    settings=concepts_settings,
)

log.info("Populating the concepts index")
for concept in Concept.nodes.all():
    log.info("Indexing concept", concept=concept.name)
    es.index(
        index=concepts_index_name,
        id=concept.uid,
        document=format_concept_for_elasticsearch(concept),
    )

people_index_name = os.environ["ELASTIC_PEOPLE_INDEX"]
log.info(f"Creating the people index: {people_index_name}")
with open("/data/elastic/people/mapping.json", "r") as f:
    people_mappings = json.load(f)
with open("/data/elastic/people/settings.json", "r") as f:
    people_settings = json.load(f)

es.indices.delete(index=people_index_name, ignore=404)
es.indices.create(
    index=people_index_name, mappings=people_mappings, settings=people_settings,
)

log.info("Populating the people index")
for person in Person.nodes.all():
    log.info("Indexing person", person=person.name)
    es.index(
        index=people_index_name,
        id=person.uid,
        document=format_person_for_elasticsearch(person),
    )
