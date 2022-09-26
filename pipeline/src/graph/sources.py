from typing import List

from . import (
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
    search_wikidata,
    get_wikidata_id_from_loc_data,
    get_wikidata_preferred_label,
    get_wikidata_variant_labels,
    get_wikipedia_label_from_wikidata,
    get_wikipedia_data,
    get_wikipedia_variant_labels,
    get_wikipedia_preferred_label,
    get_wikipedia_description,
    get_wikidata_id_from_wikipedia_data,
)
from .models import Concept, SourceConcept, SourceType

log = get_logger(__name__)


def collect_sources(
    target_concept: Concept, source_id: str, source_type: SourceType
):
    if source_type == "wikidata":
        connect_wikidata_source(
            target_concept=target_concept,
            source_id=source_id,
            get_linked_schemes=[
                "lc-subjects",
                "lc-names",
                "nlm-mesh",
                "wikipedia",
            ],
        )
    if source_type.startswith("lc-"):
        connect_loc_source(
            target_concept=target_concept,
            source_id=source_id,
            source_type=source_type,
            get_linked_schemes=["wikidata"],
        )
    if source_type == "nlm-mesh":
        connect_mesh_source(
            target_concept=target_concept,
            source_id=source_id,
            get_linked_schemes=["wikidata"],
        )
    if source_type == "label-derived":
        connect_label_derived_source(
            target_concept=target_concept, source_id=source_id
        )
    if source_type == "wikipedia":
        connect_wikipedia_source(
            target_concept=target_concept,
            source_label=source_id,
            get_linked_schemes=["wikidata"],
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
            "Error connecting label-derived source concept",
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
                connect_loc_source(
                    target_concept=target_concept,
                    source_id=loc_id,
                    source_type="lc-names",
                )
            elif loc_id.startswith("s"):
                connect_loc_source(
                    target_concept=target_concept,
                    source_id=loc_id,
                    source_type="lc-subjects",
                )
            else:
                log.exception(
                    "LoC ID does not start with 's' or 'n'", id=loc_id
                )
    if "nlm-mesh" in get_linked_schemes:
        mesh_id = get_mesh_id_from_wikidata(source_data)
        if mesh_id:
            connect_mesh_source(
                target_concept=target_concept, source_id=mesh_id
            )
    if "wikipedia" in get_linked_schemes:
        wikipedia_label = get_wikipedia_label_from_wikidata(source_data)
        if wikipedia_label:
            connect_wikipedia_source(
                target_concept=target_concept,
                source_label=wikipedia_label,
            )


def connect_wikipedia_source(
    target_concept: Concept,
    source_label: str,
    get_linked_schemes: List[SourceType] = [],
):
    try:
        wikipedia_data = get_wikipedia_data(source_label)
        source_concept = SourceConcept.nodes.get_or_none(
            source_id=source_label, source_type="wikipedia"
        )
        if not source_concept:
            log.debug(
                "Creating wikipedia source concept",
                source_id=source_label,
                source_type="wikipedia",
            )
            source_concept = SourceConcept(
                source_id=source_label,
                source_type="wikipedia",
                preferred_label=get_wikipedia_preferred_label(wikipedia_data),
                description=get_wikipedia_description(wikipedia_data),
                variant_labels=get_wikipedia_variant_labels(wikipedia_data),
            ).save()
        if not target_concept.sources.is_connected(source_concept):
            log.debug(
                "Connecting wikipedia source concept",
                concept=target_concept.label,
                source_id=source_label,
                source_type="wikipedia",
            )
            target_concept.sources.connect(source_concept)
        if "wikidata" in get_linked_schemes:
            wikidata_id = get_wikidata_id_from_wikipedia_data(wikipedia_data)
            if wikidata_id:
                connect_wikidata_source(
                    target_concept=target_concept,
                    source_id=wikidata_id,
                    get_linked_schemes=["nlm-mesh", "lc-names", "lc-subjects"],
                )
    except (ValueError) as error:
        log.exception(
            "Error connecting wikipedia source concept",
            concept=target_concept.label,
            source_label=source_label,
            error=error,
        )


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
            if not wikidata_id:
                wikidata_id = search_wikidata(source_id)
            if wikidata_id:
                connect_wikidata_source(
                    target_concept=target_concept,
                    source_id=wikidata_id,
                    get_linked_schemes=["wikipedia", "nlm-mesh"],
                )

    except (ValueError) as error:
        log.exception(
            f"Error connecting {source_type} source concept",
            concept=target_concept.label,
            loc_id=source_id,
            error=error,
        )


def connect_mesh_source(
    target_concept: Concept,
    source_id: str,
    get_linked_schemes: List[SourceType] = [],
):
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

        if "wikidata" in get_linked_schemes:
            wikidata_id = search_wikidata(source_id)
            if wikidata_id:
                connect_wikidata_source(
                    target_concept=target_concept,
                    source_id=wikidata_id,
                    get_linked_schemes=["wikipedia", "lc-names", "lc-subjects"],
                )
    except (ValueError) as error:
        log.exception(
            "Error connecting mesh source concept",
            concept=target_concept.label,
            loc_id=source_id,
            error=error,
        )
