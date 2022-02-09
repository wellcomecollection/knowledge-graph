import json
import os
from pathlib import Path

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from src.elasticsearch import (
    format_concept_for_elasticsearch,
    format_work_for_elasticsearch,
)
from src.graph import get_neo4j_session
from src.graph.models import Concept, Work
from src.utils import get_logger

log = get_logger(__name__)

data_path = Path("/data")
mappings_path = data_path / "mappings"
settings_path = data_path / "settings"

db = get_neo4j_session(clear=False)
es = Elasticsearch(
    os.environ["ELASTIC_CONCEPTS_HOST"],
    http_auth=(
        os.environ["ELASTIC_CONCEPTS_USERNAME"],
        os.environ["ELASTIC_CONCEPTS_PASSWORD"],
    ),
)


# works
works_index_name = os.environ["ELASTIC_WORKS_INDEX"]
log.info(f"Creating the works index: {works_index_name}")
with open(mappings_path / "works.json", "r") as f:
    works_mappings = json.load(f)
with open(settings_path / "works.json", "r") as f:
    works_settings = json.load(f)

es.indices.delete(index=works_index_name, ignore=404)
es.indices.create(
    index=works_index_name,
    mappings=works_mappings,
    settings=works_settings,
)

log.info("Populating the works index")
works_generator = (
    {
        "_index": works_index_name,
        "_id": work.wellcome_id,
        **format_work_for_elasticsearch(work)
    }
    for work in Work.nodes.all()
)
bulk(
    es,
    works_generator,
    chunk_size=100,
    request_timeout=60
)


# concepts
concepts_index_name = os.environ["ELASTIC_CONCEPTS_INDEX"]
log.info(f"Creating the concepts index: {concepts_index_name}")
with open(mappings_path / "concepts.json", "r") as f:
    concepts_mappings = json.load(f)
with open(settings_path / "concepts.json", "r") as f:
    concepts_settings = json.load(f)

es.indices.delete(index=concepts_index_name, ignore=404)
es.indices.create(
    index=concepts_index_name,
    mappings=concepts_mappings,
    settings=concepts_settings,
)

log.info("Populating the concepts index")
concepts_generator = (
    {
        "_index": concepts_index_name,
        "_id": concept.uid,
        **format_concept_for_elasticsearch(concept)
    }
    for concept in Concept.nodes.all()
)
bulk(
    es,
    concepts_generator,
    chunk_size=100,
    request_timeout=60
)
