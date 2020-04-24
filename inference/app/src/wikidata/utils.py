import logging
import os
import re

from . import fetch_url_json

log = logging.getLogger(__name__)


async def get_wikidata_api_response(wikidata_id):
    if not re.match("Q[0-9]+", wikidata_id):
        raise ValueError(f"{wikidata_id} is not a valid wikidata ID")

    url = f"http://www.wikidata.org/wiki/Special:EntityData/{wikidata_id}.json"
    response = await fetch_url_json(url)
    if response["object"].status == 200:
        pass
    elif response["object"].status in [400, 404]:
        raise ValueError(f"{wikidata_id} is not a valid wikidata ID")
    else:
        raise ValueError(
            f"something unexpected happened when calling url: {url}"
        )
    return response["json"]["entities"][wikidata_id]


async def find_alt_source_id_in_wikidata(alt_source_id):
    response = await fetch_url_json(
        url="https://www.wikidata.org/w/api.php",
        params={
            "action": "query",
            "list": "search",
            "srsearch": alt_source_id,
            "format": "json"
        }
    )
    if response["object"].status != 200:
        raise ValueError(f"Couldn't find '{alt_source_id}' in Wikidata")

    try:
        wikidata_id = response["json"]["query"]["search"][0]["title"]
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
        log.info(
            f"No link found between Library of Congress and Wikidata for ID: {loc_id}"
        )
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
