import os

from weco_datascience.http import fetch_redirect_url, fetch_url_json
from weco_datascience.logging import get_logger

from .library_of_congress import (get_api_response, get_lc_subjects_data,
                                  get_wikidata_id)
from .wikidata import get_wikidata_api_response

log = get_logger(__name__)


async def find_alt_source_id_in_wikidata(alt_source_id):
    response = await fetch_url_json(
        url="https://www.wikidata.org/w/api.php",
        params={
            "action": "query",
            "list": "search",
            "srsearch": alt_source_id,
            "format": "json",
        },
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
        api_response = await get_api_response(
            f"http://id.loc.gov/authorities/subjects/{loc_id}"
        )
        wikidata_id = get_wikidata_id(api_response)
        log.info(f"Found a link from LoC ID: {loc_id} to wikidata ID: {wikidata_id}")
    except ValueError:
        try:
            wikidata_id = await find_alt_source_id_in_wikidata(loc_id)
            log.info(
                f"Found a link from wikidata ID: {wikidata_id} to LoC ID: {loc_id}"
            )
        except ValueError:
            log.info(f"No link found between LoC and Wikidata for ID: {loc_id}")
            wikidata_id = None
    return wikidata_id


async def mesh_id_to_wikidata_id(mesh_id):
    try:
        wikidata_id = await find_alt_source_id_in_wikidata(mesh_id)
        log.info(f"Found a link from mesh ID: {mesh_id} to wikidata ID: {wikidata_id}")
    except ValueError:
        log.info(f"No link found between MeSH and Wikidata for ID: {mesh_id}")
        wikidata_id = None
    return wikidata_id


async def wikidata_id_to_alt_source_ids(wikidata_id):
    ids = {
        "lc_names": None,
        "lc_subjects": None,
        "mesh": None,
        "unknown": None,
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


async def unknown_label_to_loc_id(label):
    try:
        redirect_url = await fetch_redirect_url(
            "https://id.loc.gov/authorities/label/" + label
        )
        loc_id = os.path.splitext(os.path.basename(str(redirect_url)))[0]
        log.info(f"{label} = {loc_id}")
        return loc_id
    except ValueError:
        raise ValueError(f'Couldn\'t find "{label}" in LoC')


async def get_unknown_label_data(label):
    loc_id = await unknown_label_to_loc_id(label)
    return await get_lc_subjects_data(loc_id)


async def unknown_label_to_wikidata_id(label):
    loc_id = await unknown_label_to_loc_id(label)
    return await loc_id_to_wikidata_id(loc_id)
