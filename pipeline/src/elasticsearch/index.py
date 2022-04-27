import json
import os
from pathlib import Path
from time import sleep

from tqdm import tqdm

from ..graph.models import Concept, Exhibition, Work, Event
from ..utils import get_logger
from . import get_concepts_es_client
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


def create_index(client, name, mappings, settings):
    log.info(f"Creating index: {name}")
    client.indices.delete(index=name, ignore=404)
    client.indices.create(
        index=name,
        mappings=mappings,
        settings=settings,
    )


def update_mapping(client, index, mapping):
    log.info(f"Updating mapping for index: {index}")
    client.indices.put_mapping(
        index=index,
        body=mapping,
        ignore=400,
    )
    response = client.update_by_query(
        index=index,
        body={"query": {"match_all": {}}},
        wait_for_completion=False,
    )
    task_id = response["task"]
    log.info(f"Update Task ID: {task_id}")
    while task_in_progress(client, task_id):
        log.info(f"Waiting for update to complete")
        sleep(5)
    log.info(f"Update complete")


def task_in_progress(client, task_id):
    task_status = client.tasks.get(task_id)
    if task_status["completed"]:
        return False
    else:
        return True


def index_stories(start_index=0):
    concepts_es_client = get_concepts_es_client()
    log.info(
        f"Creating the stories index: {os.environ['ELASTIC_STORIES_INDEX']}"
    )
    with open(mappings_path / "stories.json", "r") as f:
        stories_mappings = json.load(f)
    with open(settings_path / "stories.json", "r") as f:
        stories_settings = json.load(f)

    if not start_index:
        concepts_es_client.indices.delete(
            index=os.environ["ELASTIC_STORIES_INDEX"], ignore=404
        )
        concepts_es_client.indices.create(
            index=os.environ["ELASTIC_STORIES_INDEX"],
            mappings=stories_mappings,
            settings=stories_settings,
        )

    log.info("Populating the stories index")
    progress_bar = tqdm(
        Work.nodes.filter(type="story"),
        total=len(Work.nodes.filter(type="story")),
        unit="stories",
    )
    for story in progress_bar:
        if progress_bar.n < start_index:
            progress_bar.set_description(f"Skipping story {story.uid}")
        else:
            progress_bar.set_description(f"Indexing story {story.uid}")
            concepts_es_client.index(
                index=os.environ["ELASTIC_STORIES_INDEX"],
                id=story.uid,
                document=format_story_for_elasticsearch(story),
            )


def index_works(start_index=0):
    concepts_es_client = get_concepts_es_client()
    log.info(f"Creating the works index: {os.environ['ELASTIC_WORKS_INDEX']}")
    with open(mappings_path / "works.json", "r") as f:
        works_mappings = json.load(f)
    with open(settings_path / "works.json", "r") as f:
        works_settings = json.load(f)

    if not start_index:
        concepts_es_client.indices.delete(
            index=os.environ["ELASTIC_WORKS_INDEX"], ignore=404
        )
        concepts_es_client.indices.create(
            index=os.environ["ELASTIC_WORKS_INDEX"],
            mappings=works_mappings,
            settings=works_settings,
        )

    log.info("Populating the works index")
    progress_bar = tqdm(
        Work.nodes.filter(type="work"),
        total=len(Work.nodes.filter(type="work")),
        unit="works",
    )
    for work in progress_bar:
        if progress_bar.n < start_index:
            progress_bar.set_description(f"Skipping work {work.uid}")
        else:
            progress_bar.set_description(f"Indexing work {work.uid}")
        concepts_es_client.index(
            index=os.environ["ELASTIC_WORKS_INDEX"],
            id=work.wellcome_id,
            document=format_work_for_elasticsearch(work),
        )


def index_concepts(start_index=0, create=False):
    concepts_es_client = get_concepts_es_client()
    index_name = os.environ["ELASTIC_SUBJECTS_INDEX"]

    if create:
        with open(mappings_path / "concepts.json", "r") as f:
            concepts_mappings = json.load(f)
        with open(settings_path / "concepts.json", "r") as f:
            concepts_settings = json.load(f)
        create_index(
            client=concepts_es_client,
            name=index_name,
            mappings=concepts_mappings,
            settings=concepts_settings,
        )

    log.info("Populating the subjects index")
    progress_bar = tqdm(
        Concept.nodes.filter(type="concept"),
        total=len(Concept.nodes.filter(type="concept")),
        unit="concepts",
    )
    for concept in progress_bar:
        if progress_bar.n < start_index:
            progress_bar.set_description(f"Skipping concept {concept.uid}")
        else:
            progress_bar.set_description(f"Indexing concept {concept.uid}")
            concepts_es_client.index(
                index=index_name,
                id=concept.uid,
                document=format_concept_for_elasticsearch(concept),
            )


def index_people(start_index=0, create=False):
    concepts_es_client = get_concepts_es_client()
    index_name = os.environ["ELASTIC_PEOPLE_INDEX"]

    if create:
        with open(mappings_path / "concepts.json", "r") as f:
            concepts_mappings = json.load(f)
        with open(settings_path / "concepts.json", "r") as f:
            concepts_settings = json.load(f)
        create_index(
            client=concepts_es_client,
            name=index_name,
            mappings=concepts_mappings,
            settings=concepts_settings,
        )

    log.info("Populating the people index")
    progress_bar = tqdm(
        Concept.nodes.filter(type="person"),
        total=len(Concept.nodes.filter(type="person")),
        unit="people",
    )

    for person in progress_bar:
        if progress_bar.n < start_index:
            progress_bar.set_description(f"Skipping person {person.uid}")
        else:
            progress_bar.set_description(f"Indexing person {person.uid}")
            concepts_es_client.index(
                index=index_name,
                id=person.uid,
                document=format_concept_for_elasticsearch(person),
            )



def index_whats_on(start_index=0, create=False):
    concepts_es_client = get_concepts_es_client()
    index_name = os.environ["ELASTIC_WHATS_ON_INDEX"]

    if create:
        with open(mappings_path / "exhibitions.json", "r") as f:
            whats_on_mappings = json.load(f)
        with open(settings_path / "exhibitions.json", "r") as f:
            whats_on_settings = json.load(f)
        create_index(
            client=concepts_es_client,
            name=index_name,
            mappings=whats_on_mappings,
            settings=whats_on_settings,
        )

    log.info("Populating the whats-on index with exhibitions")
    exhibitions_progress_bar = tqdm(
        Exhibition.nodes.all(),
        total=len(Exhibition.nodes.all()),
        unit="exhibitions",
    )

    for exhibition in exhibitions_progress_bar:
        if exhibitions_progress_bar.n < start_index:
            exhibitions_progress_bar.set_description(
                f"Skipping exhibition {exhibition.uid}"
                )
        else:
            exhibitions_progress_bar.set_description(
                f"Indexing exhibition {exhibition.uid}"
                )
            concepts_es_client.index(
                index=index_name,
                id=exhibition.uid,
                document=format_exhibition_for_elasticsearch(exhibition),
            )

    log.info("Populating the whats-on index with events")
    events_progress_bar = tqdm(
        Event.nodes.all(),
        total=len(Event.nodes.all()),
        unit="events",
    )

    for event in events_progress_bar:
        if events_progress_bar.n < start_index:
            events_progress_bar.set_description(
                f"Skipping event {event.uid}"
                )
        else:
            events_progress_bar.set_description(
                f"Indexing event {event.uid}"
                )
            concepts_es_client.index(
                index=index_name,
                id=event.uid,
                document=format_event_for_elasticsearch(event),
            )
