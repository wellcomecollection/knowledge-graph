import json
from pathlib import Path
from typing import Optional

import typer
from src.elasticsearch import get_concepts_es_client
from src.elasticsearch.index import update_mapping

app = typer.Typer()


def main(
    index: str = typer.Option(None, help="Index mapping to update"),
    path: Optional[Path] = typer.Option(
        None,
        help='Path to the mapping file, default "/data/mappings/{index}.json"',
    ),
):
    if not path:
        path = Path(f"/data/mappings/{index}.json")
    with open(path, "r") as f:
        mapping = json.load(f)

    client = get_concepts_es_client()
    update_mapping(client=client, index=index, mapping=mapping)


if __name__ == "__main__":
    typer.run(main)
