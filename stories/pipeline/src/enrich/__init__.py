from ..utils import clean, http_client

from .lcsh import (
    get_lcsh_data,
    get_lcsh_id,
    get_lcsh_preferred_name,
    get_lcsh_variant_names,
)
from .mesh import (
    get_mesh_data,
    get_mesh_description,
    get_mesh_id,
    get_mesh_preferred_name,
    get_mesh_variant_names,
)
from .wikidata import (
    get_wikidata,
    get_wikidata_description,
    get_wikidata_id,
    get_wikidata_preferred_name,
    get_wikidata_variant_names,
)


def enrich(concept_name):
    response = {
        "wikidata": {
            "id": None,
            "preferred_name": None,
            "description": None,
            "variants": [],
        },
        "lcsh": {"id": None, "preferred_name": None, "variants": [], },
        "mesh": {
            "id": None,
            "preferred_name": None,
            "description": None,
            "variants": [],
        },
    }

    response["wikidata"]["id"] = get_wikidata_id(concept_name)
    if response["wikidata"]["id"]:
        wikidata = get_wikidata(response["wikidata"]["id"])
        response["wikidata"]["variants"] = get_wikidata_variant_names(wikidata)
        response["wikidata"]["preferred_name"] = get_wikidata_preferred_name(
            wikidata
        )
        response["wikidata"]["description"] = get_wikidata_description(
            wikidata)

        response["lcsh"]["id"] = get_lcsh_id(wikidata)
        if response["lcsh"]["id"]:
            # not doing lc-names yet
            if response["lcsh"]["id"].startswith("s"):
                lcsh_data = get_lcsh_data(response["lcsh"]["id"])
                response["lcsh"]["preferred_name"] = get_lcsh_preferred_name(
                    lcsh_data
                )
                response["lcsh"]["variants"] = get_lcsh_variant_names(
                    lcsh_data)

        response["mesh"]["id"] = get_mesh_id(wikidata)
        if response["mesh"]["id"]:
            try:
                mesh_data = get_mesh_data(response["mesh"]["id"])
                response["mesh"]["preferred_name"] = get_mesh_preferred_name(
                    mesh_data
                )
                response["mesh"]["variants"] = get_mesh_variant_names(
                    mesh_data)
                response["mesh"]["description"] = get_mesh_description(
                    mesh_data
                )
            except ValueError:
                pass

    return response
