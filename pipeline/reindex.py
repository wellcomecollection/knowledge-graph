from tqdm import tqdm
import json
import os
from pathlib import Path

from elasticsearch import Elasticsearch
from elasticsearch.helpers import streaming_bulk
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

# neomodel reformulates a __len__ call as a count() cypher query, see:
# https://neo4j-examples.github.io/paradise-papers-django/tutorial/part04.html#length-of-a-nodeset
n_works = len(Work.nodes.all())
n_concepts = len(Concept.nodes.all())


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

works_progress = tqdm(unit="works", total=n_works)
successes = 0
for successful, action in streaming_bulk(
    client=es,
    actions=works_generator,
    chunk_size=10,
    request_timeout=60
):
    works_progress.update(1)
    if not successful:
        log.error(f"Failed to index work: {action['_id']}")
    else:
        successes += 1



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

concepts_progress = tqdm(unit="concepts", total=n_concepts)
successes = 0
for successful, action in streaming_bulk(
    client=es,
    actions=concepts_generator,
    chunk_size=10,
    request_timeout=60
):
    concepts_progress.update(1)
    if not successful:
        log.error(f"Failed to index concept: {action['_id']}")
    else:
        successes += 1
