from . import (
    Concept, SourceConcept,
    get_logger,
    get_wikidata,
    get_wikidata_preferred_label,
)

log = get_logger(__name__)


def get_wikidata_neighbours(target_concept: Concept, wikidata_id):
    log.debug("Getting neighbours from wikidata", source_id=wikidata_id)
    wikidata = get_wikidata(wikidata_id)
    claims = [
        # should probably add more properties to this list
        "P31",  # instance of
        "P279",  # subclass of
        "P361",  # part of
        "P527",  # has part
        "P1542",  # has effect
        "P460",  # said to be the same as
        "P2579",  # studied by
    ]
    related_ids = []
    for claim_id in claims:
        try:
            if claim_id in wikidata["claims"]:
                related_ids.extend(
                    [
                        related_claim["mainsnak"]["datavalue"]["value"]["id"]
                        for related_claim in wikidata["claims"][claim_id]
                    ]
                )
        except (KeyError, TypeError):
            continue
    for neighbour_wikidata_id in related_ids:
        log.debug(
            "Found related wikidata id", wikidata_id=neighbour_wikidata_id
        )
        neighbour_source_concept = SourceConcept.nodes.get_or_none(
            source_id=neighbour_wikidata_id, source_type="wikidata"
        )
        if neighbour_source_concept:
            log.debug(
                "Found existing wikidata neighbour source concept",
                wikidata_id=neighbour_wikidata_id,
            )
            neighbour_concept = neighbour_source_concept.parent.all()[0]
        else:
            try:
                neighbour_concept_wikidata = get_wikidata(neighbour_wikidata_id)
                label = get_wikidata_preferred_label(neighbour_concept_wikidata)
                log.info(
                    "Creating neighbour concept",
                    wikidata_id=neighbour_wikidata_id,
                    label=label,
                )
                neighbour_concept = Concept(label=label).save()
                neighbour_concept.collect_sources(
                    source_id=neighbour_wikidata_id, source_type="wikidata"
                )
            except ValueError as error:
                log.exception(
                    "Skipping neighbour, no data found",
                    wikidata_id=neighbour_wikidata_id,
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
            target_concept.neighbours.connect(neighbour_concept, {"source": "wikidata"})
