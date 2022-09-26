from . import (
    Concept,
    SourceConcept,
    Subject,
    collect_sources,
    get_logger,
    get_wikipedia_data,
    get_wikipedia_preferred_label,
    fetch_json,
)

log = get_logger(__name__)
base_url = "https://en.wikipedia.org/w/api.php"


def get_see_also_labels(wikipedia_label: str):
    sections_response = fetch_json(
        base_url,
        params={
            "action": "parse",
            "prop": "sections",
            "page": wikipedia_label,
            "format": "json",
        },
    )
    try:
        see_also_section = [
            section["index"]
            for section in sections_response["parse"]["sections"]
        ][0]
        links_response = fetch_json(
            base_url,
            params={
                "action": "parse",
                "prop": "links",
                "page": wikipedia_label,
                "section": see_also_section,
                "format": "json",
            },
        )
        see_also_labels = [
            link["*"] for link in links_response["parse"]["links"]
        ]
    except (KeyError, TypeError, IndexError):
        see_also_labels = []
    return see_also_labels


def get_wikipedia_neighbours(target_concept: Concept, wikipedia_label: str):
    wikipedia_data = get_wikipedia_data(wikipedia_label)
    try:
        category_labels = [
            category_label["title"]
            for category_label in wikipedia_data["categories"]
        ]
    except (IndexError, KeyError, TypeError):
        category_labels = []

    see_also_labels = get_see_also_labels(wikipedia_label)
    for neighbour_wikipedia_label in category_labels + see_also_labels:
        log.debug(
            "Found related wikipedia page",
            wikipedia_label=neighbour_wikipedia_label,
        )
        neighbour_source_concept = SourceConcept.nodes.get_or_none(
            source_id=neighbour_wikipedia_label, source_type="wikipedia"
        )
        if neighbour_source_concept:
            log.debug(
                "Found existing wikipedia neighbour source concept",
                wikipedia_label=neighbour_wikipedia_label,
            )
            neighbour_concept = neighbour_source_concept.parent.all()[0]
        else:
            try:
                neighbour_concept_wikipedia_data = get_wikipedia_data(
                    neighbour_wikipedia_label
                )
                label = get_wikipedia_preferred_label(
                    neighbour_concept_wikipedia_data
                )
                log.info(
                    "Creating neighbour concept",
                    wikidata_id=neighbour_wikipedia_label,
                    label=label,
                )
                neighbour_concept = Subject(label=label).save()
                collect_sources(
                    target_concept=neighbour_concept,
                    source_id=neighbour_wikipedia_label,
                    source_type="wikipedia",
                )
            except ValueError as error:
                log.exception(
                    "Skipping neighbour, no data found",
                    wikidata_id=neighbour_wikipedia_label,
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
                neighbour_concept, {"source": "wikipedia"}
            )
