import re
import requests
import logging

log = logging.getLogger(__name__)


def get_wikidata_api_response(wikidata_id):
    if not re.match("Q[0-9]+", wikidata_id):
        raise ValueError(f"{wikidata_id} is not a valid wikidata ID")

    url = f"http://www.wikidata.org/wiki/Special:EntityData/{wikidata_id}.json"
    api_response = requests.get(url)
    if api_response.status_code == 200:
        pass
    elif api_response.status_code in [400, 404]:
        raise ValueError(f"{wikidata_id} is not a valid wikidata ID")
    else:
        raise ValueError(
            f"something unexpected happened when calling url: {url}"
        )
    return api_response.json()["entities"][wikidata_id]


def get_wikidata_data(wikidata_id):
    api_response = get_wikidata_api_response(wikidata_id)

    label = get_label(api_response)
    description = get_description(api_response)
    variants = get_variants(api_response)
    birth_date = get_birth_date(api_response)
    death_date = get_death_date(api_response)

    log.info(f"Got data from wikidata for ID: {wikidata_id}")

    return {
        "id": wikidata_id,
        "title": label,
        "description": description,
        "birth_date": birth_date,
        "death_date": death_date,
        "variants": variants
    }


def get_label(api_response):
    try:
        label = api_response["labels"]["en"]["value"]
    except KeyError:
        log.info(f"Couldn't find label for ID: {api_response['id']}")
        label = None
    return label


def get_description(api_response):
    try:
        description = api_response["descriptions"]["en"]["value"]
    except KeyError:
        log.info(f"Couldn't find description for ID: {api_response['id']}")
        description = None
    return description


def get_variants(api_response):
    try:
        variants = [alias["value"] for alias in api_response["aliases"]["en"]]
    except KeyError:
        log.info(f"Couldn't find variants for ID: {api_response['id']}")
        variants = []
    return variants


def get_birth_date(api_response):
    try:
        birth_date = api_response["claims"]["P569"][0]["mainsnak"]["datavalue"]["value"]["time"]
    except KeyError:
        log.info(f"Couldn't find birth date for ID: {api_response['id']}")
        birth_date = None
    return birth_date


def get_death_date(api_response):
    try:
        death_date = api_response["claims"]["P570"][0]["mainsnak"]["datavalue"]["value"]["time"]
    except KeyError:
        log.info(f"Couldn't find death date for ID: {api_response['id']}")
        death_date = None
    return death_date
