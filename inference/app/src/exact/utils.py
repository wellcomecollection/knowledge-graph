import os
import requests
from .lc_names import get_lc_names_api_response
from .wikidata import get_wikidata_api_response


def find_alt_source_id_in_wikidata(alt_source_id):
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


def lc_names_id_to_wikidata_id(lc_names_id):
    try:
        wikidata_id = find_alt_source_id_in_wikidata(lc_names_id)
    except ValueError:
        raise ValueError(
            f"No link found between Library of Congress and Wikidata for ID: {lc_names_id}"
        )
    return wikidata_id


def mesh_id_to_wikidata_id(mesh_id):
    try:
        wikidata_id = find_alt_source_id_in_wikidata(mesh_id)
    except ValueError:
        raise ValueError(
            f"No link found between MeSH and Wikidata for ID: {mesh_id}"
        )
    return wikidata_id


def wikidata_id_to_alt_source_ids(wikidata_id):
    ids = {
        "lc_names": None,
        "lc_subjects": None,
        "mesh": None
    }
    api_response = get_wikidata_api_response(wikidata_id)
    claims = api_response["claims"]

    try:
        loc_id = claims["P244"][0]["mainsnak"]["datavalue"]["value"]
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
