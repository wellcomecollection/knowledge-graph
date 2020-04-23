import logging
from copy import deepcopy

from .exact.lc_names import get_lc_names_data
from .exact.lc_subjects import get_lc_subjects_data
from .exact.mesh import get_mesh_data
from .exact.utils import (loc_id_to_wikidata_id, mesh_id_to_wikidata_id,
                          wikidata_id_to_alt_source_ids)
from .exact.wikidata import get_wikidata_data

log = logging.getLogger(__name__)

blank_response = {
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


def aggregate(query_id, id_type):
    response = deepcopy(blank_response)
    if id_type == "lc_names":
        response["exact"]["lc_names"] = get_lc_names_data(query_id)
        wikidata_id = loc_id_to_wikidata_id(query_id)
    elif id_type == "lc_subjects":
        response["exact"]["lc_subjects"] = get_lc_subjects_data(query_id)
        wikidata_id = loc_id_to_wikidata_id(query_id)
    elif id_type == "mesh":
        response["exact"]["mesh"] = get_mesh_data(query_id)
        wikidata_id = mesh_id_to_wikidata_id(query_id)
    elif id_type == "wikidata":
        wikidata_id = query_id
    else:
        raise ValueError(f"{id_type} is not a valid id_type")

    if wikidata_id:
        response["exact"]["wikidata"] = get_wikidata_data(wikidata_id)

        alt_source_ids = wikidata_id_to_alt_source_ids(wikidata_id)

        if alt_source_ids["lc_subjects"] and not response["exact"]["lc_subjects"]:
            lc_subjects_id = alt_source_ids["lc_subjects"]
            response["exact"]["lc_subjects"] = get_lc_subjects_data(
                lc_subjects_id
            )

        if alt_source_ids["lc_names"] and not response['exact']['lc_names']:
            lc_names_id = alt_source_ids["lc_names"]
            response["exact"]["lc_names"] = get_lc_names_data(lc_names_id)

        if alt_source_ids["mesh"] and not response['exact']['mesh']:
            mesh_id = alt_source_ids["mesh"]
            response["exact"]["mesh"] = get_mesh_data(mesh_id)

    return response
