import logging

from .library_of_congress import get_lc_names_data, get_lc_subjects_data
from .mesh import get_mesh_data
from .utils import (loc_id_to_wikidata_id, mesh_id_to_wikidata_id,
                    wikidata_id_to_alt_source_ids)
from .wikidata import get_wikidata_data
from .logging import get_logger

log = get_logger(__name__)


async def _aggregate(query_id, id_type):
    response = {
        "exact": {
            "lc_names": None,
            "lc_subjects": None,
            "mesh": None,
            "wikidata": None
        },
        "inferred": {
            "lc_names": None,
            "lc_subjects": None,
            "mesh": None,
            "wikidata": None
        }
    }

    if id_type == "lc_names":
        response["lc_names"] = await get_lc_names_data(query_id)
        wikidata_id = await loc_id_to_wikidata_id(query_id)
    elif id_type == "lc_subjects":
        response["exact"]["lc_subjects"] = await get_lc_subjects_data(query_id)
        wikidata_id = await loc_id_to_wikidata_id(query_id)
    elif id_type == "mesh":
        response["exact"]["mesh"] = await get_mesh_data(query_id)
        wikidata_id = await mesh_id_to_wikidata_id(query_id)
    elif id_type == "wikidata":
        wikidata_id = query_id
    else:
        raise ValueError(f"{id_type} is not a valid id_type")

    if wikidata_id:
        response["exact"]["wikidata"] = await get_wikidata_data(wikidata_id)

        alt_source_ids = await wikidata_id_to_alt_source_ids(wikidata_id)

        if alt_source_ids["lc_subjects"] and not response["exact"]["lc_subjects"]:
            lc_subjects_id = alt_source_ids["lc_subjects"]
            response["exact"]["lc_subjects"] = await get_lc_subjects_data(
                lc_subjects_id
            )

        if alt_source_ids["lc_names"] and not response['exact']['lc_names']:
            lc_names_id = alt_source_ids["lc_names"]
            response["exact"]["lc_names"] = await get_lc_names_data(lc_names_id)

        if alt_source_ids["mesh"] and not response['exact']['mesh']:
            mesh_id = alt_source_ids["mesh"]
            response["exact"]["mesh"] = await get_mesh_data(mesh_id)

    return response


async def aggregate_wikidata(wikidata_id, label_type):
    wikidata = {
        "label": wikidata_id,
        "label_type": "wikidata_id",
        "children": []
    }

    response = await get_wikidata_data(wikidata_id)
    names = [
        name for name in response["variants"] + [response["title"]] if name
    ]
    for variant in names:
        wikidata["children"].append({
            "label": variant,
            "label_type": "name",
            "children": []
        })

    alt_source_ids = await wikidata_id_to_alt_source_ids(wikidata_id)

    if alt_source_ids["lc_subjects"] and label_type != "lc_subjects":
        lc_subjects_data = {
            "label": alt_source_ids["lc_subjects"],
            "label_type": "lc_subjects_id",
            "children": []
        }
        response = await get_lc_subjects_data(alt_source_ids["lc_subjects"])
        names = [
            name for name in response["variants"] + [response["title"]] if name
        ]
        for variant in names:
            lc_subjects_data["children"].append({
                "label": variant,
                "label_type": "name",
                "children": []
            })

        wikidata["children"].append(lc_subjects_data)

    if alt_source_ids["lc_names"] and label_type != "lc_names":
        lc_names_data = {
            "label": alt_source_ids["lc_names"],
            "label_type": "lc_names_id",
            "children": []
        }
        response = await get_lc_names_data(alt_source_ids["lc_names"])
        names = [
            name for name in response["variants"] + [response["title"]] if name
        ]
        for variant in names:
            lc_names_data["children"].append({
                "label": variant,
                "label_type": "name",
                "children": []
            })

        wikidata["children"].append(lc_names_data)

    if alt_source_ids["mesh"] and label_type != "mesh":
        mesh_data = {
            "label": alt_source_ids["mesh"],
            "label_type": "mesh_id",
            "children": []
        }
        response = await get_mesh_data(alt_source_ids["mesh"])
        names = [
            name for name in response["variants"] + [response["title"]] if name
        ]
        for variant in names:
            mesh_data["children"].append({
                "label": variant,
                "label_type": "name",
                "children": []
            })

        wikidata["children"].append(mesh_data)

    return wikidata


async def aggregate(label, label_type):
    enriched_concept = {
        "label": label,
        "label_type": label_type,
        "children": []
    }

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
    names = [
        name for name in response["variants"] + [response["title"]] if name
    ]
    for variant in names:
        enriched_concept["children"].append({
            "label": variant,
            "label_type": "name",
            "children": []
        })

    if wikidata_id:
        wikidata = await aggregate_wikidata(wikidata_id, label_type)
        enriched_concept["children"].append(wikidata)

    return enriched_concept
