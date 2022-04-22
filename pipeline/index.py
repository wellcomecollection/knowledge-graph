from structlog import get_logger
import typer
from src.elasticsearch.index import (
    index_concepts,
    index_people,
    index_stories,
    index_works,
    index_exhibitions,
    index_events

)
from src.graph import get_neo4j_session

app = typer.Typer()

db = get_neo4j_session()

log = get_logger()

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
    exhibitions: int = typer.Option(
        0, help="Reindex exhibitions from the given position onwards"
    ),
    events: int = typer.Option(
        0, 
        help="Reindex events from the given position onwards"
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
    if exhibitions:
        index_exhibitions(exhibitions)
    if events:
        index_events(events)

    if not any([stories, works, concepts, people, exhibitions, events]):
        index_stories(stories)
        index_works(works)
        index_concepts(concepts)
        index_people(people)
        index_exhibitions(exhibitions)
        index_events(events)


if __name__ == "__main__":
    typer.run(main)
