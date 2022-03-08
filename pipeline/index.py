import typer

from src.elasticsearch.index import (
    index_concepts,
    index_people,
    index_stories,
    index_works,
)
from src.graph import get_neo4j_session

app = typer.Typer()

db = get_neo4j_session()


def main(
    stories: int = typer.Option(
        0, help="Reindex stories from the given position onwards"
    ),
    works: int = typer.Option(
        0, help="Reindex works from the given position onwards"
    ),
    concepts: int = typer.Option(
        0, help="Reindex concepts from the given position onwards"
    ),
    people: int = typer.Option(
        0, help="Reindex people from the given position onwards"
    ),
):
    """
    Reindex data from the graph store into elasticsearch. Using flags to
    specify a node type will only reindex those nodes, while no flags will
    reindex all nodes.
    """
    if stories:
        index_stories(stories)
    if works:
        index_works(works)
    if concepts:
        index_concepts(concepts)
    if people:
        index_people(people)

    if not any([stories, works, concepts, people]):
        index_stories(stories)
        index_works(works)
        index_concepts(concepts)
        index_people(people)


if __name__ == "__main__":
    typer.run(main)
