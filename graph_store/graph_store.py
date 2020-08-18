import typer
from src.elastic import ES
from src.graph import Graph
from src.logging import get_logger
from src.enrich import get_enriched_concept, traverse

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

    for concept in es.get_concepts_data():
        if "ids" in concept["_source"]:
            for id in concept["_source"]["ids"]:
                if "lc-names" in id or "lc-subjects" in id or "nlm-mesh" in id:
                    authority, authority_id = id.split("/")
                    enriched_concept = get_enriched_concept(
                        authority, authority_id
                    )
                    for node in traverse(enriched_concept):
                        graph.create_node(node["child"])
                        if node["parent"]:
                            graph.create_edge(node["parent"], node["child"])


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


if __name__ == "__main__":
    app()
