from src.graph import get_neo4j_session
from src.graph.models import SourceConcept, Subject
from src.graph.neighbours import get_neighbours
from src.utils import get_logger
from tqdm import tqdm

log = get_logger(__name__)
get_neo4j_session()


def connect_concept_neighbours(concept):
    try:
        concept.get_neighbours()
    except SessionExpired as error:
        log.exception("Session expired. Reconnecting...", error=error)
        get_neo4j_session()
        connect_concept_neighbours(concept)


orphans = SourceConcept.nodes.has(parent=False)
log.info(f"Found {len(orphans)} orphans")
for orphan in orphans:
    parent = Subject(label=orphan.preferred_label).save()
    parent.sources.connect(orphan)


log.info("Getting second order concepts and connections")

first_order_concepts = Subject.nodes.has(
    works=True, sources=True, neighbours=False
)

n = len(first_order_concepts)
log.info(f"Found {n} first order concepts")

for concept in tqdm(first_order_concepts):
    get_neighbours(target_concept=concept)
