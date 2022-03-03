import json
import os
from pathlib import Path

from tqdm import tqdm

from elasticsearch import Elasticsearch
from src.elasticsearch import (
    format_concept_for_elasticsearch,
    format_story_for_elasticsearch,
    format_work_for_elasticsearch,
)
from src.graph import get_neo4j_session
from src.graph.models import Concept, Work
from src.utils import get_logger

log = get_logger(__name__)

data_path = Path("/data")
mappings_path = data_path / "mappings"
settings_path = data_path / "settings"

db = get_neo4j_session()
es = Elasticsearch(
    os.environ["ELASTIC_CONCEPTS_HOST"],
    http_auth=(
        os.environ["ELASTIC_CONCEPTS_USERNAME"],
        os.environ["ELASTIC_CONCEPTS_PASSWORD"],
    ),
)

STORIES_START_POSITION = 0
WORKS_START_POSITION = 0
CONCEPTS_START_POSITION = 0
PEOPLE_START_POSITION = 0

# # stories
# stories_index_name = os.environ["ELASTIC_STORIES_INDEX"]
# log.info(f"Creating the stories index: {stories_index_name}")
# with open(mappings_path / "stories.json", "r") as f:
#     stories_mappings = json.load(f)
# with open(settings_path / "stories.json", "r") as f:
#     stories_settings = json.load(f)

# if not STORIES_START_POSITION:
#     es.indices.delete(index=stories_index_name, ignore=404)
#     es.indices.create(
#         index=stories_index_name,
#         mappings=stories_mappings,
#         settings=stories_settings,
#     )

# log.info("Populating the stories index")
# progress_bar = tqdm(
#     Work.nodes.filter(type="story"),
#     total=len(Work.nodes.filter(type="story")),
#     unit="stories",
# )
# for story in progress_bar:
#     if progress_bar.n < STORIES_START_POSITION:
#         progress_bar.set_description(f"Skipping story {story.uid}")
#     else:
#         progress_bar.set_description(f"Indexing story {story.uid}")
#         es.index(
#             index=stories_index_name,
#             id=story.uid,
#             document=format_story_for_elasticsearch(story),
#         )


# # works
# works_index_name = os.environ["ELASTIC_WORKS_INDEX"]
# log.info(f"Creating the works index: {works_index_name}")
# with open(mappings_path / "works.json", "r") as f:
#     works_mappings = json.load(f)
# with open(settings_path / "works.json", "r") as f:
#     works_settings = json.load(f)

# if not WORKS_START_POSITION:
#     es.indices.delete(index=works_index_name, ignore=404)
#     es.indices.create(
#         index=works_index_name,
#         mappings=works_mappings,
#         settings=works_settings,
#     )

# log.info("Populating the works index")
# progress_bar = tqdm(
#     Work.nodes.filter(type="work"),
#     total=len(Work.nodes.filter(type="work")),
#     unit="works",
# )
# for work in progress_bar:
#     if progress_bar.n < WORKS_START_POSITION:
#         progress_bar.set_description(f"Skipping work {work.uid}")
#     else:
#         progress_bar.set_description(f"Indexing work {work.uid}")
#     es.index(
#         index=works_index_name,
#         id=work.wellcome_id,
#         document=format_work_for_elasticsearch(work),
#     )

# concepts
concepts_index_name = os.environ["ELASTIC_CONCEPTS_INDEX"]
log.info(f"Creating the concepts index: {concepts_index_name}")
with open(mappings_path / "concepts.json", "r") as f:
    concepts_mappings = json.load(f)
with open(settings_path / "concepts.json", "r") as f:
    concepts_settings = json.load(f)

if not CONCEPTS_START_POSITION:
    es.indices.delete(index=concepts_index_name, ignore=404)
    es.indices.create(
        index=concepts_index_name,
        mappings=concepts_mappings,
        settings=concepts_settings,
    )

log.info("Populating the concepts index")
progress_bar = tqdm(
    Concept.nodes.filter(type="concept"),
    total=len(Concept.nodes.filter(type="concept")),
    unit="concepts",
)
for concept in progress_bar:
    if progress_bar.n < CONCEPTS_START_POSITION:
        progress_bar.set_description(f"Skipping concept {concept.uid}")
    else:
        progress_bar.set_description(f"Indexing concept {concept.uid}")
        es.index(
            index=concepts_index_name,
            id=concept.uid,
            document=format_concept_for_elasticsearch(concept),
        )

# people
concepts_index_name = os.environ["ELASTIC_CONCEPTS_INDEX"]
with open(mappings_path / "concepts.json", "r") as f:
    concepts_mappings = json.load(f)
with open(settings_path / "concepts.json", "r") as f:
    concepts_settings = json.load(f)

log.info("Populating the concepts index")
progress_bar = tqdm(
    Concept.nodes.filter(type="person"),
    total=len(Concept.nodes.filter(type="person")),
    unit="people",
)

for person in progress_bar:
    if progress_bar.n < PEOPLE_START_POSITION:
        progress_bar.set_description(f"Skipping person {person.uid}")
    else:
        progress_bar.set_description(f"Indexing person {person.uid}")
        es.index(
            index=concepts_index_name,
            id=person.uid,
            document=format_concept_for_elasticsearch(person),
        )
