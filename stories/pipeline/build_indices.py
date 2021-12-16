import json
import os

from structlog import get_logger

from src.elasticsearch import (
    format_concept_for_elasticsearch,
    format_story_for_elasticsearch,
    format_person_for_elasticsearch,
    get_elasticsearch_session,
)
from src.graph.models import Concept, Story, Person

log = get_logger()
log.info("Unpacking the graph into elasticsearch")
es = get_elasticsearch_session()


stories_index_name = os.environ["ELASTIC_STORIES_INDEX"]
log.info(f"Create the stories index: {stories_index_name}")
with open("/data/elastic/stories/mapping.json", "r") as f:
    stories_mappings = json.load(f)
with open("/data/elastic/stories/settings.json", "r") as f:
    stories_settings = json.load(f)

es.indices.delete(index=stories_index_name, ignore=404)
es.indices.create(
    index=stories_index_name,
    mappings=stories_mappings,
    settings=stories_settings,
)

log.info("Populating the stories index")
for story in Story.nodes.all():
    log.info("Indexing story", story=story.title)
    es.index(
        index=stories_index_name,
        id=story.wellcome_id,
        document=format_story_for_elasticsearch(story),
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

