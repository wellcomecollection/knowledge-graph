import logging

from .library_of_congress import get_lc_names_data, get_lc_subjects_data
from .logging import get_logger
from .mesh import get_mesh_data
from .node import Node
from .utils import (loc_id_to_wikidata_id, mesh_id_to_wikidata_id,
                    wikidata_id_to_alt_source_ids)
from .wikidata import get_wikidata_data

log = get_logger(__name__)

THIRD_PARTIES = (
    ("lc_subjects", get_lc_subjects_data),
    ("lc_names", get_lc_names_data),
    ("mesh", get_mesh_data),
)


async def aggregate_wikidata(wikidata_id, label_type):
    wikidata = Node(label=wikidata_id, label_type=wikidata_id)
    response = await get_wikidata_data(wikidata_id)
    for variant in response["variants"] + [response["title"]]:
        wikidata.add_child(variant)

    alt_source_ids = await wikidata_id_to_alt_source_ids(wikidata_id)

    for label_type, get_data in THIRD_PARTIES:
        if alt_source_ids[label_type] and label_type != label_type:
            lc_subjects_data = Node(
                label=alt_source_ids[label_type],
                label_type=label_type + "_id"
            )
            response = await get_data(alt_source_ids[label_type])
            for variant in response["variants"] + [response["title"]]:
                lc_subjects_data.add_child(variant)

            wikidata.add_child(lc_subjects_data)

    return wikidata


async def aggregate(label, label_type):
    enriched_concept = Node(label, label_type)

    if label_type == "lc_names":
        response = await get_lc_names_data(label)
        wikidata_id = await loc_id_to_wikidata_id(label)
    elif label_type == "lc_subjects":
        response = await get_lc_subjects_data(label)
        wikidata_id = await loc_id_to_wikidata_id(label)
    elif label_type == "mesh":
        response = await get_mesh_data(label)
        wikidata_id = await mesh_id_to_wikidata_id(label)
    elif label_type == "wikidata":
        enriched_concept = await aggregate_wikidata(label, label_type)
        return enriched_concept
    else:
        raise ValueError(f"{label_type} is not a valid label_type")

    for variant in response["variants"] + [response["title"]]:
        enriched_concept.add_child(variant)

    if wikidata_id:
        wikidata = await aggregate_wikidata(wikidata_id, label_type)
        enriched_concept.add_child(wikidata)

    return enriched_concept
