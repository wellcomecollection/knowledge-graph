# Should be tweaked to specify the nodes, index, fields, etc to be updated

import os

from src.elasticsearch import get_concepts_es_client
from src.elasticsearch.format import ordered_source_preferences
from src.graph import get_neo4j_session
from src.graph.models import Concept
from tqdm import tqdm

db = get_neo4j_session()
concepts_es_client = get_concepts_es_client()


progress_bar = tqdm(
    Concept.nodes.filter(type="concept"),
    total=len(Concept.nodes.filter(type="concept")),
    unit="concepts",
)
for concept in progress_bar:
    progress_bar.set_description(f"Updating concept {concept.uid}")
    neighbour_names = []
    for neighbour in concept.neighbours:
        preferred_name = neighbour.name
        for source_type in ordered_source_preferences:
            source = neighbour.sources.get_or_none(source_type=source_type)
            if source:
                preferred_name = source.preferred_name
                break
        neighbour_names.append(preferred_name)

    concepts_es_client.update(
        index=os.environ["ELASTIC_CONCEPTS_INDEX"],
        id=concept.uid,
        doc={
            "neighbour_names": neighbour_names,
            "neighbour_ids": [
                neighbour.uid for neighbour in concept.neighbours
            ],
        },
    )
