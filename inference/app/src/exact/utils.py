import os
import requests
from .lc_names import get_lc_names_api_response


def get_wikidata_id_from_loc(lc_names_id, api_response=None):
    api_response = api_response or get_lc_names_api_response(lc_names_id)

    wikidata_id = None
    for element in api_response:
        if element["@id"].startswith("http://www.wikidata.org/entity/"):
            wikidata_id = os.path.basename(element["@id"])

    if not wikidata_id:
        raise ValueError(
            "Couldn't find a Wikidata ID in Library of Congress data"
        )

    return wikidata_id


def get_wikidata_id_from_wikidata(lc_names_id):
    response = requests.get(
        url="https://www.wikidata.org/w/api.php",
        params={
            "action": "query",
            "list": "search",
            "srsearch": lc_names_id,
            "format": "json"
        }
    ).json()

    try:
        first_result = response["query"]["search"][0]
        wikidata_id = first_result["title"]
    except (KeyError, IndexError):
        raise ValueError(f"Couldn't find '{lc_names_id}' in Wikidata")

    return wikidata_id


def lc_names_id_to_wikidata_id(lc_names_id, api_response=None):
    try:
        wikidata_id = get_wikidata_id_from_loc(lc_names_id, api_response)
    except ValueError:
        try:
            wikidata_id = get_wikidata_id_from_wikidata(lc_names_id)
        except ValueError:
            raise ValueError(
                f"No link found between Library of Congress and Wikidata for ID: {lc_names_id}"
            )
    return wikidata_id
