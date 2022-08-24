import os

import typer

from src.elasticsearch import get_concepts_es_client
from src.elasticsearch.index import (
    index_people,
    index_stories,
    index_subjects,
    index_whats_on,
    index_works,
)
from src.elasticsearch.manage import index_exists
from src.graph import get_neo4j_session

app = typer.Typer()

db = get_neo4j_session()


def main(
    stories: bool = typer.Option(False, "--stories", help="Index stories"),
    works: bool = typer.Option(False, "--works", help="Index works"),
    subjects: bool = typer.Option(False, "--subjects", help="Index subjects"),
    people: bool = typer.Option(False, "--people", help="Index people"),
    whats_on: bool = typer.Option(False, "--whats-on", help="Index whats on"),
):
    """
    Reindex data from the graph store into elasticsearch. Using flags to
    specify a node type will only reindex those nodes, while no flags will
    reindex all nodes.
    """
    client = get_concepts_es_client()

    if stories:
        index = os.environ["ELASTIC_STORIES_INDEX"]
        if index_exists(client=client, index=index):
            if not typer.confirm(
                f"{index} already exists. Are you sure you want to proceed? The existing index will be deleted.",
            ):
                return
        index_stories(client=client, index=index)

    if works:
        index = os.environ["ELASTIC_WORKS_INDEX"]
        if index_exists(client=client, index=index):
            if not typer.confirm(
                f"{index} already exists. Are you sure you want to proceed? The existing index will be deleted.",
            ):
                return
        index_works(client=client, index=index)

    if subjects:
        index = os.environ["ELASTIC_SUBJECTS_INDEX"]
        if index_exists(client=client, index=index):
            if not typer.confirm(
                f"{index} already exists. Are you sure you want to proceed? The existing index will be deleted.",
            ):
                return
        index_subjects(client=client, index=index)

    if people:
        index = os.environ["ELASTIC_PEOPLE_INDEX"]
        if index_exists(client=client, index=index):
            if not typer.confirm(
                f"{index} already exists. Are you sure you want to proceed? The existing index will be deleted.",
            ):
                return
        index_people(client=client, index=index)

    if whats_on:
        index = os.environ["ELASTIC_WHATS_ON_INDEX"]
        if index_exists(client=client, index=index):
            if not typer.confirm(
                f"{index} already exists. Are you sure you want to proceed? The existing index will be deleted.",
            ):
                return
        index_whats_on(client=client, index=index)

    if not any([stories, works, subjects, people, whats_on]):
        if typer.confirm(
            "Are you sure you want to reindex all nodes?",
        ):
            index_stories(
                client=client, index=os.environ["ELASTIC_STORIES_INDEX"]
            )
            index_works(client=client, index=os.environ["ELASTIC_WORKS_INDEX"])
            index_subjects(
                client=client, index=os.environ["ELASTIC_SUBJECTS_INDEX"]
            )
            index_people(
                client=client, index=os.environ["ELASTIC_PEOPLE_INDEX"]
            )
            index_whats_on(
                client=client, index=os.environ["ELASTIC_WHATS_ON_INDEX"]
            )
        else:
            return


if __name__ == "__main__":
    typer.run(main)
