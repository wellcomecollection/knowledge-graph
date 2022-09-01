from .. import get_logger
from ..enrich import (
    get_loc_data,
    get_loc_preferred_label,
    get_mesh_data,
    get_mesh_preferred_label,
    get_wikidata,
    get_wikidata_preferred_label,
    get_wikipedia_data,
    get_wikipedia_preferred_label,
)
from ..models import Concept, SourceConcept
from .loc import get_loc_neighbours
from .mesh import get_mesh_neighbours
from .wikidata import get_wikidata_neighbours
from .wikipedia import get_wikipedia_neighbours

log = get_logger(__name__)


def get_neighbours(target_concept: Concept):
    log.info("Getting neighbours for concept", concept=target_concept.label)
    for source_concept in target_concept.sources.all():
        if source_concept.source_type == "wikidata":
            get_wikidata_neighbours(
                target_concept, wikidata_id=source_concept.source_id
            )
        elif (
            source_concept.source_type == "lc-subjects"
            or source_concept.source_type == "lc-names"
        ):
            get_loc_neighbours(
                target_concept,
                source_id=source_concept.source_id,
            )
        elif source_concept.source_type == "nlm-mesh":
            get_mesh_neighbours(
                target_concept, mesh_id=source_concept.source_id
            )
