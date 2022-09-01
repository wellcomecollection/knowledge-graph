from pathlib import Path

from . import (
    Concept,
    SourceConcept,
    get_logger,
    get_mesh_data,
    get_mesh_preferred_label,
)

log = get_logger(__name__)


def get_mesh_neighbours(target_concept: Concept, mesh_id: str):
    try:
        mesh_data = get_mesh_data(mesh_id)
        related_ids = []
        keys = [
            "seeAlso",
            "hasDescriptor",
            "hasQualifier",
            "broaderDescriptor",
            "broaderQualifier",
        ]
        for key in keys:
            if key in mesh_data:
                if isinstance(mesh_data[key], list):
                    related_ids.extend(
                        [Path(related).name for related in mesh_data[key]]
                    )
                elif isinstance(mesh_data[key], str):
                    related_ids.append(Path(mesh_data[key]).name)

        for neighbour_mesh_id in related_ids:
            log.debug("Found related mesh id", mesh_id=neighbour_mesh_id)
            neighbour_source_concept = SourceConcept.nodes.get_or_none(
                source_id=neighbour_mesh_id, source_type="nlm-mesh"
            )
            if neighbour_source_concept:
                log.debug(
                    "Found existing mesh neighbour source concept",
                    mesh_id=neighbour_mesh_id,
                )
                neighbour_concept = neighbour_source_concept.parent.all()[0]
            else:
                try:
                    neighbour_concept_mesh_data = get_mesh_data(
                        neighbour_mesh_id
                    )
                    label = get_mesh_preferred_label(
                        neighbour_concept_mesh_data
                    )
                    log.info(
                        "Creating neighbour concept",
                        mesh_id=neighbour_mesh_id,
                        label=label,
                    )
                    neighbour_concept = Concept(label=label).save()
                    neighbour_concept.collect_sources(
                        source_id=neighbour_mesh_id, source_type="nlm-mesh"
                    )
                except ValueError as error:
                    log.exception(
                        "Skipping neighbour, no data found",
                        neighbour_mesh_id=neighbour_mesh_id,
                        message=error,
                    )
                    continue

            if neighbour_concept == target_concept:
                log.debug(
                    "Skipping neighbour, concept is the same",
                    concept_label=target_concept.label,
                    neighbour_label=neighbour_concept.label,
                )
                continue
            else:
                log.debug(
                    "Connecting neighbour",
                    concept_label=target_concept.label,
                    neighbour_label=neighbour_concept.label,
                )
                target_concept.neighbours.connect(
                    neighbour_concept, {"source": "nlm-mesh"}
                )
    except TypeError as error:
        log.error(
            "Error getting mesh neighbours",
            mesh_id=mesh_id,
            error=error,
        )
