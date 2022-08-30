from pathlib import Path
from time import sleep

from elasticsearch import Elasticsearch, NotFoundError

from ..utils import get_logger

data_path = Path("/data")
mappings_path = data_path / "mappings"
settings_path = data_path / "settings"

log = get_logger(__name__)


def index_exists(client: Elasticsearch, index: str):
    try:
        client.indices.get(index)
        return True
    except NotFoundError:
        return False


def delete_index(client: Elasticsearch, index: str):
    if index_exists(client, index):
        log.info(f"Deleting index: {index}")
        client.indices.delete(index=index)


def create_index(client: Elasticsearch, index: str, mappings, settings):
    log.info(f"Creating index: {index}")
    client.indices.create(
        index=index,
        mappings=mappings,
        settings=settings,
    )


def update_mapping(client: Elasticsearch, index: str, mapping):
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
        log.info("Waiting for update to complete")
        sleep(5)
    log.info("Update complete")


def task_in_progress(client: Elasticsearch, task_id: str):
    task_status = client.tasks.get(task_id)
    if task_status["completed"]:
        return False
    else:
        return True
