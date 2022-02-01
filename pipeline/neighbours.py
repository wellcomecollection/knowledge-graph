from src.utils import get_logger

from src.graph import get_neo4j_session
from src.graph.models import Concept

log = get_logger(__name__)
db = get_neo4j_session(clear=False)

log.info("Getting second order concepts and connections")

first_order_concepts = Concept.nodes.has(
    works=True, sources=True, neighbours=False
)
second_order_concepts = Concept.nodes.has(
    works=False, sources=True, neighbours=True
)

for concept in first_order_concepts:
    concept.get_neighbours()
