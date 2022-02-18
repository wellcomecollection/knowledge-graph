from src.graph import get_neo4j_session
from src.graph.models import Concept, SourceConcept
from src.utils import get_logger

log = get_logger(__name__)
db = get_neo4j_session()

orphans = SourceConcept.nodes.has(parent=False)
log.info(f"Found {len(orphans)} orphans")
for orphan in orphans:
    parent = Concept(name=orphan.preferred_name, type="concept").save()
    parent.sources.connect(orphan)

log.info("Getting second order concepts and connections")

first_order_concepts = Concept.nodes.has(
    works=True, sources=True, neighbours=False
)

n = len(first_order_concepts)
log.info(f"Found {n} first order concepts")

for i, concept in enumerate(first_order_concepts):
    log.info(f"{i+1}/{n}")
    concept.get_neighbours()
