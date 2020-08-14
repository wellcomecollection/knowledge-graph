import typer
from src.elastic import ES
from src.graph import Graph
from src.logging import get_logger
from src.enrich import enrich

log = get_logger(__name__)
app = typer.Typer()


@app.command()
def populate(
    start: int = typer.Option(0, help=(
        "The number of results already in the graph store - useful if you're "
        "populating in batches rather than in one go"
    ))
):
    """
    Basic ETL pipeline for the graph store.

    Extract data from the elasticsearch concepts index, apply a minimal
    transformation, and load it into the neo4j aura graph store.
    """
    graph = Graph()
    es = ES()
    i = 0
    for concept in es.get_concepts_data():
        i += 1
        if i < start:
            log.info("Skipping " + concept["_source"]["label"])
            pass
        else:
            graph.create_node(concept["_source"])


@app.command()
def clear(
    limit: int = typer.Option(None, help=(
        "The number of nodes to delete if aura times out while trying to get "
        "rid of them all in one go"
    ))
):
    """Remove all nodes and edges from the graph."""
    if typer.confirm("Are you sure you want to clear the graph store?"):
        Graph().clear(limit=limit)


@app.command()
def get_stats():
    """Get some headline statistics about the data in the graph store"""
    response = Graph().get_stats()
    print(response)


@app.command()
def test_enrichment():
    enrich("lc-names", "nb2015021801")


if __name__ == "__main__":
    app()
