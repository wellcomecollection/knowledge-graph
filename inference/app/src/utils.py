import logging
import os

import requests

from .wikidata import get_wikidata_api_response

log = logging.getLogger(__name__)


async def find_alt_source_id_in_wikidata(alt_source_id):
    response = requests.get(
        url="https://www.wikidata.org/w/api.php",
        params={
            "action": "query",
            "list": "search",
            "srsearch": alt_source_id,
            "format": "json"
        }
    ).json()

    try:
        wikidata_id = response["query"]["search"][0]["title"]
    except (KeyError, IndexError):
        raise ValueError(f"Couldn't find '{alt_source_id}' in Wikidata")
    return wikidata_id


async def loc_id_to_wikidata_id(loc_id):
    try:
        wikidata_id = await find_alt_source_id_in_wikidata(loc_id)
        log.info(
            f"Found a link from LoC ID: {loc_id} to wikidata ID: {wikidata_id}"
        )
    except ValueError:
        log.info(f"No link found between Library of Congress and Wikidata for ID: {loc_id}")
        wikidata_id = None
    return wikidata_id


async def mesh_id_to_wikidata_id(mesh_id):
    try:
        wikidata_id = await find_alt_source_id_in_wikidata(mesh_id)
        log.info(
            f"Found a link from mesh ID: {mesh_id} to wikidata ID: {wikidata_id}"
        )
    except ValueError:
        log.info(f"No link found between MeSH and Wikidata for ID: {mesh_id}")
        wikidata_id = None
    return wikidata_id


async def wikidata_id_to_alt_source_ids(wikidata_id):
    ids = {
        "lc_names": None,
        "lc_subjects": None,
        "mesh": None
    }
    api_response = await get_wikidata_api_response(wikidata_id)
    claims = api_response["claims"]

    try:
        loc_id = claims["P244"][0]["mainsnak"]["datavalue"]["value"]
        # TODO: make sure these assertions about id format are actually true
        if loc_id.startswith("sh"):
            ids["lc_subjects"] = loc_id
        elif loc_id.startswith("n"):
            ids["lc_names"] = loc_id
    except KeyError:
        pass

    try:
        ids["mesh"] = claims["P486"][0]["mainsnak"]["datavalue"]["value"]
    except KeyError:
        pass

    return ids
