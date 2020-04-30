import logging

from .exact.lc_names import get_lc_names_data
from .exact.mesh import get_mesh_data
from .exact.utils import lc_names_id_to_wikidata_id, mesh_id_to_wikidata_id, wikidata_id_to_alt_source_ids
from .exact.wikidata import get_wikidata_data

log = logging.getLogger(__name__)


def aggregate_lc_names_data(lc_names_id):
    response = {
        'exact': {},
        'inferred': {}
    }
    response['exact']['lc_names'] = get_lc_names_data(lc_names_id)
    log.info(f"Got data from lc_names for ID: {lc_names_id}")

    try:
        wikidata_id = lc_names_id_to_wikidata_id(lc_names_id)
        log.info(
            f'Found a link from lc_names ID: {lc_names_id} to wikidata ID: {wikidata_id}'
        )
    except ValueError:
        log.info(f"Couldn't find a wikidata record for ID: {lc_names_id}")

    if wikidata_id:
        response['exact']['wikidata'] = get_wikidata_data(wikidata_id)
        log.info(f"Got data from wikidata for ID: {wikidata_id}")

        alt_source_ids = wikidata_id_to_alt_source_ids(wikidata_id)
        if alt_source_ids['mesh']:
            mesh_id = alt_source_ids['mesh']
            response['exact']['mesh'] = get_mesh_data(mesh_id)

    return response


def aggregate_mesh_data(mesh_id):
    response = {
        'exact': {},
        'inferred': {}
    }

    response['exact']['mesh'] = get_mesh_data(mesh_id)
    log.info(f"Got data from MeSH for ID: {mesh_id}")

    try:
        wikidata_id = mesh_id_to_wikidata_id(mesh_id)
        log.info(
            f'Found a link from mesh ID: {mesh_id} to wikidata ID: {wikidata_id}'
        )
    except ValueError:
        log.info(f"Couldn't find a wikidata record for ID: {mesh_id}")

    if wikidata_id:
        response['exact']['wikidata'] = get_wikidata_data(wikidata_id)
        log.info(f"Got data from wikidata for ID: {wikidata_id}")

        alt_source_ids = wikidata_id_to_alt_source_ids(wikidata_id)
        if alt_source_ids['lc_names']:
            lc_names_id = alt_source_ids['lc_names']
            response['exact']['lc_names'] = get_lc_names_data(lc_names_id)

    return response
