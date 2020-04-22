import logging
import os

import requests

log = logging.getLogger(__name__)


def get_lc_names_api_response(lc_names_id):
    entity_url = f"http://id.loc.gov/authorities/names/{lc_names_id}"
    api_response = requests.get(entity_url + '.json')
    if api_response.status_code == 200:
        pass
    elif api_response.status_code == 404:
        raise ValueError(f"{lc_names_id} is not a valid lc_names ID")
    else:
        raise ValueError(
            f"something unexpected happened when calling url: {entity_url}"
        )

    for element in api_response.json():
        if element["@id"] == entity_url:
            return element


def get_lc_names_data(lc_names_id):
    api_response = get_lc_names_api_response(lc_names_id)
    try:
        label = api_response["http://www.loc.gov/mads/rdf/v1#authoritativeLabel"][0]["@value"]
    except (KeyError, IndexError):
        log.info(f"Couldn't find label for ID: {lc_names_id}")
        label = None

    try:
        variants = [
            altlabel["@value"]
            for altlabel in api_response["http://www.w3.org/2004/02/skos/core#altLabel"]
        ]
    except KeyError:
        log.info(f"Couldn't find variants for ID: {lc_names_id}")
        variants = []

    log.info(f"Got data from lc_names for ID: {lc_names_id}")

    return {
        "id": lc_names_id,
        "title": label,
        "variants": variants
    }
