import re
from .http import fetch_url_json
import logging

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


async def get_wikidata_data(wikidata_id):
    api_response = await get_wikidata_api_response(wikidata_id)

    label = await get_label(api_response)
    description = await get_description(api_response)
    variants = await get_variants(api_response)
    birth_date = await get_birth_date(api_response)
    death_date = await get_death_date(api_response)
    broader_concepts = await get_broader_concepts(api_response)

    log.info(f"Got data from wikidata for ID: {wikidata_id}")

    return {
        "id": wikidata_id,
        "title": label,
        "description": description,
        "birth_date": birth_date,
        "death_date": death_date,
        "variants": variants,
        "broader_concepts": broader_concepts,
    }


async def get_label(api_response):
    try:
        label = api_response["labels"]["en"]["value"]
    except KeyError:
        log.info(f"Couldn't find label for ID: {api_response['id']}")
        label = None
    return label


async def get_description(api_response):
    try:
        description = api_response["descriptions"]["en"]["value"]
    except KeyError:
        log.info(f"Couldn't find description for ID: {api_response['id']}")
        description = None
    return description


async def get_variants(api_response):
    try:
        variants = [alias["value"] for alias in api_response["aliases"]["en"]]
    except KeyError:
        log.info(f"Couldn't find variants for ID: {api_response['id']}")
        variants = None
    return variants


async def get_birth_date(api_response):
    try:
        birth_date = api_response["claims"]["P569"][0]["mainsnak"]["datavalue"]["value"]["time"]
    except KeyError:
        log.info(f"Couldn't find birth date for ID: {api_response['id']}")
        birth_date = None
    return birth_date


async def get_death_date(api_response):
    try:
        death_date = api_response["claims"]["P570"][0]["mainsnak"]["datavalue"]["value"]["time"]
    except KeyError:
        log.info(f"Couldn't find death date for ID: {api_response['id']}")
        death_date = None
    return death_date


async def get_broader_concepts(api_response):
    try:
        broader_concept_ids = [
            element["mainsnak"]["datavalue"]["value"]["id"]
            for element in api_response["claims"]["P31"]
        ]
        broader_concept_responses = [
            await get_wikidata_api_response(id) for id in broader_concept_ids
        ]
        broader_concepts = [
            await get_label(response) for response in broader_concept_responses
        ]
    except KeyError:
        log.info(
            f"Couldn't find broader concepts for ID: {api_response['id']}")
        broader_concepts = None
    return broader_concepts
