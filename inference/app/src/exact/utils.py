import os
import requests
from .lc_names import get_lc_names_api_response


def get_wikidata_id_from_loc(lc_names_id):
    api_response = get_lc_names_api_response(lc_names_id)

    wikidata_id = None
    for element in api_response:
        if element["@id"].startswith("http://www.wikidata.org/entity/"):
            wikidata_id = os.path.basename(element["@id"])

    if not wikidata_id:
        raise ValueError(
            "Couldn't find a Wikidata ID in Library of Congress data"
        )

    return wikidata_id


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
        wikidata_id = get_wikidata_id_from_loc(lc_names_id)
    except ValueError:
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
