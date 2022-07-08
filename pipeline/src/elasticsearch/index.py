import json
from pathlib import Path
from elasticsearch import Elasticsearch
from tqdm import tqdm

from ..elasticsearch.manage import create_index, delete_index

from ..graph.models import Concept, Exhibition, Work, Event
from ..utils import get_logger
from .format import (
    format_concept_for_elasticsearch,
    format_story_for_elasticsearch,
    format_work_for_elasticsearch,
    format_exhibition_for_elasticsearch,
    format_event_for_elasticsearch,
)

data_path = Path("/data")
mappings_path = data_path / "mappings"
settings_path = data_path / "settings"

log = get_logger(__name__)


def index_stories(client: Elasticsearch, index: str):
    log.info(f"Creating the stories index: {index}")
    with open(mappings_path / "stories.json", "r", encoding="utf-8") as f:
        mappings = json.load(f)
    with open(settings_path / "stories.json", "r", encoding="utf-8") as f:
        settings = json.load(f)

    delete_index(client, index)
    create_index(client, index, mappings, settings)

    log.info("Populating the stories index")
    stories = Work.nodes.filter(type="story")
    progress_bar = tqdm(stories, total=len(stories), unit="stories")
    for story in progress_bar:
        progress_bar.set_description(f"Indexing story {story.uid}")
        client.index(
            index=index,
            id=story.wellcome_id,
            document=format_story_for_elasticsearch(story),
        )


def index_works(client: Elasticsearch, index: str):
    log.info(f"Creating the works index: {index}")
    with open(mappings_path / "works.json", "r", encoding="utf-8") as f:
        mappings = json.load(f)
    with open(settings_path / "works.json", "r", encoding="utf-8") as f:
        settings = json.load(f)

    delete_index(client, index)
    create_index(client, index, mappings, settings)

    log.info("Populating the works index")
    progress_bar = tqdm(
        Work.nodes.filter(type="work"),
        total=len(Work.nodes.filter(type="work")),
        unit="works",
    )
    for work in progress_bar:

        client.index(
            index=index,
            id=work.wellcome_id,
            document=format_work_for_elasticsearch(work),
        )


def index_subjects(client: Elasticsearch, index: str):
    log.info(f"Creating the subjects index: {index}")
    with open(mappings_path / "subjects.json", "r", encoding="utf-8") as f:
        mappings = json.load(f)
    with open(settings_path / "subjects.json", "r", encoding="utf-8") as f:
        settings = json.load(f)

    delete_index(client, index)
    create_index(client, index, mappings, settings)

    log.info(f"Populating index: {index}")
    concepts = Concept.nodes.filter(type="concept").has(works=True)
    progress_bar = tqdm(
        concepts,
        total=len(concepts),
        unit="concepts",
    )
    for concept in progress_bar:
        progress_bar.set_description(f"Indexing concept {concept.uid}")
        client.index(
            index=index,
            id=concept.uid,
            document=format_concept_for_elasticsearch(concept),
        )


def index_people(client: Elasticsearch, index: str):
    log.info(f"Creating index: {index}")
    with open(mappings_path / "people.json", "r", encoding="utf-8") as f:
        mappings = json.load(f)
    with open(settings_path / "people.json", "r", encoding="utf-8") as f:
        settings = json.load(f)

    delete_index(client, index)
    create_index(client, index, mappings, settings)

    log.info(f"Populating index: {index}")
    people = Concept.nodes.filter(type="person")
    progress_bar = tqdm(people, total=len(people), unit="people")
    for person in progress_bar:
        progress_bar.set_description(f"Indexing person {person.uid}")
        client.index(
            index=index,
            id=person.uid,
            document=format_concept_for_elasticsearch(person),
        )


def index_whats_on(client: Elasticsearch, index: str):
    log.info(f"Creating index: {index}")
    with open(mappings_path / "people.json", "r", encoding="utf-8") as f:
        mappings = json.load(f)
    with open(settings_path / "people.json", "r", encoding="utf-8") as f:
        settings = json.load(f)

    delete_index(client, index)
    create_index(client, index, mappings, settings)

    log.info(f"Populating index: {index}")
    exhibitions = Exhibition.nodes.all()
    exhibitions_progress_bar = tqdm(
        exhibitions, total=len(exhibitions), unit="exhibitions"
    )

    for exhibition in exhibitions_progress_bar:
        exhibitions_progress_bar.set_description(
            f"Indexing exhibition {exhibition.uid}"
        )
        client.index(
            index=index,
            id=exhibition.uid,
            document=format_exhibition_for_elasticsearch(exhibition),
        )

    events = Event.nodes.all()
    events_progress_bar = tqdm(events, total=len(events), unit="events")
    for event in events_progress_bar:
        events_progress_bar.set_description(f"Indexing event {event.uid}")
        client.index(
            index=index,
            id=event.uid,
            document=format_event_for_elasticsearch(event),
        )
