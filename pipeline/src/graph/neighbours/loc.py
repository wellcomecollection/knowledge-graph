from pathlib import Path

from . import (
    Concept,
    SourceConcept,
    get_loc_data,
    get_loc_preferred_label,
    get_logger,
)

log = get_logger(__name__)


def get_loc_neighbours(target_concept: Concept, source_id: str):
    loc_data = get_loc_data(source_id)
    related_ids = []
    keys = [
        "http://www.w3.org/2004/02/skos/core#broader",
        "http://www.w3.org/2004/02/skos/core#narrower",
    ]
    for key in keys:
        if key in loc_data:
            related_ids.extend(
                [Path(authority["@id"]).name for authority in loc_data[key]]
            )
    if "http://www.loc.gov/mads/rdf/v1#componentList" in loc_data:
        related_ids.extend(
            [
                Path(component["@id"]).name
                for component in loc_data[
                    "http://www.loc.gov/mads/rdf/v1#componentList"
                ][0]["@list"]
            ]
        )

    for neighbour_loc_id in related_ids:
        log.debug("Found related loc id", loc_id=neighbour_loc_id)
        neighbour_source_concept = SourceConcept.nodes.get_or_none(
            source_id=neighbour_loc_id
        )
        if neighbour_source_concept:
            log.debug(
                "Found existing neighbour source concept",
                loc_id=neighbour_loc_id,
            )
            neighbour_concept = neighbour_source_concept.parent.all()[0]
        else:
            try:
                neighbour_concept_loc_data = get_loc_data(neighbour_loc_id)
                label = get_loc_preferred_label(neighbour_concept_loc_data)
                log.info(
                    "Creating neighbour concept",
                    loc_id=neighbour_loc_id,
                    label=label,
                )
                neighbour_concept = Concept(label=label).save()
                neighbour_concept.collect_sources(
                    source_id=neighbour_loc_id,
                    source_type=(
                        "lc-subjects"
                        if neighbour_loc_id.startswith("s")
                        else "lc-names"
                    ),
                )
            except (ValueError) as error:
                log.exception(
                    "Skipping neighbour, no data found",
                    neighbour_loc_id=neighbour_loc_id,
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
                neighbour_concept,
                {
                    "source": "lc-subjects"
                    if neighbour_loc_id.startswith("s")
                    else "lc-names"
                },
            )
