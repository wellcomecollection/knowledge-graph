import logging
import os

import requests

log = logging.getLogger(__name__)


def get_api_response(url):
    api_response = requests.get(url + '.json')
    if api_response.status_code == 200:
        pass
    elif api_response.status_code == 404:
        loc_id = os.path.basename(url)
        raise ValueError(f"{loc_id} is not a valid library of congress ID")
    else:
        raise ValueError(
            f"something unexpected happened when calling url: {url}"
        )

    for element in api_response.json():
        if element["@id"] == url:
            return element


def get_variants(api_response):
    try:
        variants = [
            altlabel["@value"] for altlabel in
            api_response["http://www.w3.org/2004/02/skos/core#altLabel"]
        ]
    except KeyError:
        lc_subjects_id = os.path.basename(api_response['@id'])
        log.info(f"Couldn't find variants for ID: {lc_subjects_id}")
        variants = []
    return variants


def get_label(api_response):
    try:
        label = api_response["http://www.loc.gov/mads/rdf/v1#authoritativeLabel"][0]["@value"]
    except (KeyError, IndexError):
        lc_subjects_id = os.path.basename(api_response['@id'])
        log.info(f"Couldn't find label for ID: {lc_subjects_id}")
        label = None
    return label


def get_hierarchical_concepts(api_response, direction):
    lc_names_id = os.path.basename(api_response['@id'])
    response_element_id = f'http://www.loc.gov/mads/rdf/v1#has{direction}Authority'
    try:
        elements = api_response[response_element_id]
    except KeyError:
        log.info(
            f"Couldn't find {direction.lower()} concepts for ID: {lc_names_id}"
        )
        return None

    urls = [element['@id'] for element in elements]
    responses = [get_api_response(url) for url in urls]
    hierarchical_concepts = [get_label(response) for response in responses]

    log.info(f'Got {direction.lower()} concepts for ID: {lc_names_id}')
    return hierarchical_concepts


def get_lc_subjects_data(lc_subjects_id):
    url = f"http://id.loc.gov/authorities/subjects/{lc_subjects_id}"
    api_response = get_api_response(url)

    label = get_label(api_response)
    variants = get_variants(api_response)
    broader_concepts = get_hierarchical_concepts(api_response, 'Broader')
    narrower_concepts = get_hierarchical_concepts(api_response, 'Narrower')

    log.info(f"Got data from lc_subjects for ID: {lc_subjects_id}")
    return {
        "id": lc_subjects_id,
        "title": label,
        "variants": variants,
        "broader_concepts": broader_concepts,
        "narrower_concepts": narrower_concepts,
    }


def get_lc_names_data(lc_names_id):
    url = f"http://id.loc.gov/authorities/names/{lc_names_id}"
    api_response = get_api_response(url)
    label = get_label(api_response)
    variants = get_variants(api_response)

    log.info(f"Got data from lc_names for ID: {lc_names_id}")

    return {
        "id": lc_names_id,
        "title": label,
        "variants": variants
    }
