
import asyncio
import os
import time

from .http import fetch_url_json
from .logging import get_logger

log = get_logger(__name__)


async def get_api_response(url):
    try:
        response = await fetch_url_json(url + '.json')
    except ValueError as e:
        raise e
    if response["object"].status == 200:
        pass
    elif response["object"].status == 404:
        loc_id = os.path.basename(url)
        raise ValueError(f"{loc_id} is not a valid library of congress ID")
    else:
        raise ValueError(
            f"something unexpected happened when calling url: {url}"
        )

    for element in response["json"]:
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
        log.debug(f"Couldn't find variants for ID: {lc_subjects_id}")
        variants = []
    return variants


def get_label(api_response):
    try:
        label = api_response["http://www.loc.gov/mads/rdf/v1#authoritativeLabel"][0]["@value"]
    except (KeyError, IndexError):
        lc_subjects_id = os.path.basename(api_response['@id'])
        log.debug(f"Couldn't find label for ID: {lc_subjects_id}")
        label = None
    return label


async def get_hierarchical_concepts(api_response, direction):
    start_time = time.time()
    lc_names_id = os.path.basename(api_response['@id'])
    response_element_id = f'http://www.loc.gov/mads/rdf/v1#has{direction}Authority'
    try:
        elements = api_response[response_element_id]
    except KeyError:
        log.debug(
            f"Couldn't find {direction.lower()} concepts for ID: {lc_names_id}"
        )
        return None

    responses = await asyncio.gather(
        *[get_api_response(element['@id']) for element in elements]
    )

    concepts = [get_label(response) for response in responses]

    log.debug(
        f'Got {direction.lower()} concepts for ID: {lc_names_id}'
        f', which took took {round(time.time() - start_time, 2)}s'
    )

    return concepts


async def get_lc_subjects_data(lc_subjects_id):
    url = f"http://id.loc.gov/authorities/subjects/{lc_subjects_id}"
    api_response = await get_api_response(url)

    label = get_label(api_response)
    variants = get_variants(api_response)
    broader_concepts = await get_hierarchical_concepts(api_response, 'Broader')
    narrower_concepts = await get_hierarchical_concepts(api_response, 'Narrower')

    log.info(f"Got data from lc_subjects for ID: {lc_subjects_id}")
    return {
        "id": lc_subjects_id,
        "title": label,
        "variants": variants,
        "broader_concepts": broader_concepts,
        "narrower_concepts": narrower_concepts,
    }


async def get_lc_names_data(lc_names_id):
    url = f"http://id.loc.gov/authorities/names/{lc_names_id}"
    api_response = await get_api_response(url)
    label = get_label(api_response)
    variants = get_variants(api_response)

    log.info(f"Got data from lc_names for ID: {lc_names_id}")

    return {
        "id": lc_names_id,
        "title": label,
        "variants": variants
    }
