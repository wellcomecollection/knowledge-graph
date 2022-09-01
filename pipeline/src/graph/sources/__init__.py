from typing import List

from .. import (
    get_loc_data,
    get_loc_id_from_wikidata,
    get_loc_preferred_label,
    get_loc_variant_labels,
    get_logger,
    get_mesh_data,
    get_mesh_description,
    get_mesh_id_from_wikidata,
    get_mesh_preferred_concept_data,
    get_mesh_preferred_label,
    get_wikidata,
    get_wikidata_description,
    get_wikidata_id_from_loc_data,
    get_wikidata_preferred_label,
    get_wikidata_variant_labels,
    get_wikipedia_data,
)
from ..models import Concept, SourceConcept, SourceType

log = get_logger(__name__)


def collect_sources(target_concept: Concept, source_id, source_type):
    if source_type == "wikidata":
        connect_wikidata_source(
            target_concept=target_concept,
            source_id=source_id,
            get_linked_schemes=["lc-subjects", "lc-names", "nlm-mesh"],
        )
    if source_type.startswith("lc-"):
        connect_loc_source(
            target_concept=target_concept,
            source_id=source_id,
            source_type=source_type,
            get_linked_schemes=["wikidata"],
        )
    if source_type == "nlm-mesh":
        connect_mesh_source(target_concept=target_concept, source_id=source_id)
    if source_type == "label-derived":
        connect_label_derived_source(
            target_concept=target_concept, source_id=source_id
        )


def connect_label_derived_source(target_concept: Concept, source_id: str):
    try:
        source_concept = SourceConcept.nodes.get_or_none(
            source_id=source_id, source_type="label-derived"
        )
        if not source_concept:
            log.debug(
                "Creating source concept",
                source_id=source_id,
                source_type="label-derived",
            )
            source_concept = SourceConcept(
                source_id=source_id,
                source_type="label-derived",
                preferred_label=target_concept.label,
                variant_labels=[],
            ).save()
        if not target_concept.sources.is_connected(source_concept):
            log.debug(
                "Connecting source concept",
                concept=target_concept.label,
                source_id=source_id,
                source_type="label-derived",
            )
            target_concept.sources.connect(source_concept)
    except (ValueError) as error:
        log.exception(
            f"Error connecting label-derived source concept",
            concept=target_concept.label,
            loc_id=source_id,
            error=error,
        )


def connect_wikidata_source(
    target_concept: Concept,
    source_id: str,
    get_linked_schemes: List[SourceType] = [],
):
    source_data = get_wikidata(source_id)
    source_concept = SourceConcept.nodes.get_or_none(
        source_id=source_id, source_type="wikidata"
    )
    if not source_concept:
        log.debug("Creating wikidata source concept", wikidata_id=source_id)
        source_concept = SourceConcept(
            source_id=source_id,
            source_type="wikidata",
            description=get_wikidata_description(source_data),
            preferred_label=get_wikidata_preferred_label(source_data),
            variant_labels=get_wikidata_variant_labels(source_data),
        ).save()
    if not target_concept.sources.is_connected(source_concept):
        log.debug(
            "Connecting wikidata source concept",
            concept=target_concept.label,
            wikidata_id=source_id,
        )
        target_concept.sources.connect(source_concept)

    if "lc-subjects" in get_linked_schemes or "lc-names" in get_linked_schemes:
        loc_id = get_loc_id_from_wikidata(source_data)
        if loc_id:
            if loc_id.startswith("n"):
                target_concept._connect_loc_source(
                    source_id=loc_id, source_type="lc-names"
                )
            if loc_id.startswith("s"):
                target_concept._connect_loc_source(
                    source_id=loc_id, source_type="lc-subjects"
                )
    if "nlm-mesh" in get_linked_schemes:
        mesh_id = get_mesh_id_from_wikidata(source_data)
        if mesh_id:
            target_concept._connect_mesh_source(mesh_id)


def connect_wikipedia_source(
    target_concept: Concept,
    wikipedia_id: str,
    get_linked_schemes: List[SourceType] = [],
):
    source_data = get_wikipedia_data(wikipedia_id)
    pass


def connect_loc_source(
    target_concept: Concept,
    source_id: str,
    source_type: SourceType,
    get_linked_schemes: List[SourceType] = [],
):
    try:
        loc_data = get_loc_data(source_id)
        source_concept = SourceConcept.nodes.get_or_none(
            source_id=source_id, source_type=source_type
        )
        if not source_concept:
            log.debug(
                "Creating source concept",
                source_id=source_id,
                source_type=source_type,
            )
            source_concept = SourceConcept(
                source_id=source_id,
                source_type=source_type,
                preferred_label=get_loc_preferred_label(loc_data),
                variant_labels=get_loc_variant_labels(loc_data),
            ).save()
        if not target_concept.sources.is_connected(source_concept):
            log.debug(
                "Connecting source concept",
                concept=target_concept.label,
                source_id=source_id,
                source_type=source_type,
            )
            target_concept.sources.connect(source_concept)

        if "wikidata" in get_linked_schemes:
            wikidata_id = get_wikidata_id_from_loc_data(loc_data)
            if wikidata_id:
                target_concept._connect_wikidata_source(
                    wikidata_id, get_linked_schemes=["nlm-mesh"]
                )
    except (ValueError) as error:
        log.exception(
            f"Error connecting {source_type} source concept",
            concept=target_concept.label,
            loc_id=source_id,
            error=error,
        )


def connect_mesh_source(target_concept: Concept, source_id: str):
    try:
        source_data = get_mesh_data(source_id)
        source_concept = SourceConcept.nodes.get_or_none(
            source_id=source_id, source_type="nlm-mesh"
        )
        if not source_concept:
            source_data = get_mesh_preferred_concept_data(source_data)
            log.debug("Creating mesh source concept", mesh_id=source_id)
            source_concept = SourceConcept(
                source_id=source_id,
                source_type="nlm-mesh",
                description=get_mesh_description(source_data),
                preferred_label=get_mesh_preferred_label(source_data),
                variant_labels=[],
            ).save()
        if not target_concept.sources.is_connected(source_concept):
            log.debug(
                "Connecting mesh source concept",
                concept=target_concept.label,
                mesh_id=source_id,
            )
            target_concept.sources.connect(source_concept)
    except (ValueError) as error:
        log.exception(
            "Error connecting mesh source concept",
            concept=target_concept.label,
            loc_id=source_id,
            error=error,
        )
