from string import ascii_letters

from src.graph import get_neo4j_session
from src.graph.models import SourceConcept
from src.utils import get_logger

log = get_logger(__name__)
db = get_neo4j_session()

results, meta = db.cypher_query(
    """
    MATCH ()-[r:HAS_SOURCE_CONCEPT]-(n:SourceConcept)
    WITH n, count(r) as rel_cnt
    WHERE rel_cnt > 1
    RETURN n
    """
)

source_concepts_with_duplicate_parents = [
    SourceConcept.inflate(row[0]) for row in results
]

for source_concept in source_concepts_with_duplicate_parents:
    parents = source_concept.parent.all()
    parent_labels = [parent.label for parent in parents]
    uids = [parent.uid for parent in parents]
    formatted_matches = [
        f"({ascii_letters[i]}:Concept {{uid:'{uid}'}})"
        for i, uid in enumerate(uids)
    ]

    log.info(
        "Found duplicate source concept",
        uid=source_concept.uid,
        type=source_concept.source_type,
        label=source_concept.preferred_label,
        parents=parent_labels,
    )

    query = f"""
        MATCH {', '.join(formatted_matches)}
        WITH head(collect([{','.join(uids)}])) as nodes
        CALL apoc.refactor.mergeNodes(nodes,{{
            properties:"overwrite",
            mergeRels:true
        }})
        YIELD node
        RETURN count(*)
        """
    print(query)
    db.cypher_query(query)
    log.info("Merged duplicate source concept")
