import logging

from .exact.lc_names import get_lc_names_data
from .exact.lc_subjects import get_lc_subjects_data
from .exact.mesh import get_mesh_data
from .exact.utils import (loc_id_to_wikidata_id, mesh_id_to_wikidata_id,
                          wikidata_id_to_alt_source_ids)
from .exact.wikidata import get_wikidata_data

log = logging.getLogger(__name__)


def aggregate_lc_names(lc_names_id):
    response = {
        "exact": {},
        "inferred": {}
    }
    response["exact"]["lc_names"] = get_lc_names_data(lc_names_id)
    log.info(f"Got data from lc_names for ID: {lc_names_id}")

    try:
        wikidata_id = loc_id_to_wikidata_id(lc_names_id)
        log.info(
            f"Found a link from lc_names ID: {lc_names_id} to wikidata ID: {wikidata_id}"
        )
    except ValueError:
        wikidata_id = None
        log.info(f"Couldn't find a wikidata record for ID: {lc_names_id}")

    if wikidata_id:
        response["exact"]["wikidata"] = get_wikidata_data(wikidata_id)
        log.info(f"Got data from wikidata for ID: {wikidata_id}")

        alt_source_ids = wikidata_id_to_alt_source_ids(wikidata_id)
        if alt_source_ids["mesh"]:
            mesh_id = alt_source_ids["mesh"]
            response["exact"]["mesh"] = get_mesh_data(mesh_id)

    return response


def aggregate_lc_subjects(lc_subjects_id):
    response = {
        "exact": {},
        "inferred": {}
    }
    response["exact"]["lc_subjects"] = get_lc_subjects_data(lc_subjects_id)
    log.info(f"Got data from lc_subjects for ID: {lc_subjects_id}")

    try:
        wikidata_id = loc_id_to_wikidata_id(lc_subjects_id)
        log.info(
            f"Found a link from lc_subjects ID: {lc_subjects_id} to wikidata ID: {wikidata_id}"
        )
    except ValueError:
        wikidata_id = None
        log.info(f"Couldn't find a wikidata record for ID: {lc_subjects_id}")

    if wikidata_id:
        response["exact"]["wikidata"] = get_wikidata_data(wikidata_id)
        log.info(f"Got data from wikidata for ID: {wikidata_id}")

        alt_source_ids = wikidata_id_to_alt_source_ids(wikidata_id)
        if alt_source_ids["mesh"]:
            mesh_id = alt_source_ids["mesh"]
            response["exact"]["mesh"] = get_mesh_data(mesh_id)

    return response


def aggregate_mesh(mesh_id):
    response = {
        "exact": {},
        "inferred": {}
    }

    response["exact"]["mesh"] = get_mesh_data(mesh_id)
    log.info(f"Got data from MeSH for ID: {mesh_id}")

    try:
        wikidata_id = mesh_id_to_wikidata_id(mesh_id)
        log.info(
            f"Found a link from mesh ID: {mesh_id} to wikidata ID: {wikidata_id}"
        )
    except ValueError:
        wikidata_id = None
        log.info(f"Couldn't find a wikidata record for ID: {mesh_id}")

    if wikidata_id:
        response["exact"]["wikidata"] = get_wikidata_data(wikidata_id)
        log.info(f"Got data from wikidata for ID: {wikidata_id}")

        alt_source_ids = wikidata_id_to_alt_source_ids(wikidata_id)
        if alt_source_ids["lc_names"]:
            lc_names_id = alt_source_ids["lc_names"]
            response["exact"]["lc_names"] = get_lc_names_data(lc_names_id)

    return response


def aggregate_wikidata(wikidata_id):
    response = {
        "exact": {},
        "inferred": {}
    }

    response["exact"]["wikidata"] = get_wikidata_data(wikidata_id)
    log.info(f"Got data from wikidata for ID: {wikidata_id}")

    alt_source_ids = wikidata_id_to_alt_source_ids(wikidata_id)
    print(alt_source_ids)
    if alt_source_ids["lc_names"]:
        lc_names_id = alt_source_ids["lc_names"]
        response["exact"]["lc_names"] = get_lc_names_data(lc_names_id)
    if alt_source_ids["mesh"]:
        mesh_id = alt_source_ids["mesh"]
        response["exact"]["mesh"] = get_mesh_data(mesh_id)

    return response
