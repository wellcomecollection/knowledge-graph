from ..utils import clean
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
    wikidata_id = get_wikidata_id(concept_name)
    wikidata = get_wikidata(wikidata_id)
    wikidata_preferred_name = get_wikidata_preferred_name(wikidata)
    wikidata_variants = get_wikidata_variant_names(wikidata)
    wikidata_description = get_wikidata_description(wikidata)

    lcsh_id = get_lcsh_id(wikidata)
    lcsh_data = get_lcsh_data(lcsh_id)
    lcsh_preferred_name = get_lcsh_preferred_name(lcsh_data)
    lcsh_variants = get_lcsh_variant_names(lcsh_data)

    mesh_id = get_mesh_id(wikidata)
    mesh_data = get_mesh_data(mesh_id)
    mesh_preferred_name = get_mesh_preferred_name(mesh_data)
    mesh_variants = get_mesh_variant_names(mesh_data)
    mesh_description = get_mesh_description(mesh_data)

    return {
        "wikidata": {
            "id": wikidata_id,
            "preferred_name": wikidata_preferred_name,
            "description": wikidata_description,
            "variants": wikidata_variants,
        },
        "lcsh": {
            "id": lcsh_id,
            "preferred_name": lcsh_preferred_name,
            "variants": lcsh_variants,
        },
        "mesh": {
            "id": mesh_id,
            "preferred_name": mesh_preferred_name,
            "description": mesh_description,
            "variants": mesh_variants,
        },
    }
