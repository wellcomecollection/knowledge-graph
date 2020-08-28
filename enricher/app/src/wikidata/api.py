import asyncio
import re
import time

from weco_datascience.http import fetch_url_json
from weco_datascience.logging import get_logger

log = get_logger(__name__)

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
            f"something unexpected happened when calling url: {url}")
    return response["json"]["entities"][wikidata_id]


def get_title(api_response):
    try:
        title = api_response["labels"]["en"]["value"]
    except KeyError:
        log.debug(f"Couldn't find title for ID: {api_response['id']}")
        title = None
    return title


def get_description(api_response):
    try:
        description = api_response["descriptions"]["en"]["value"]
    except KeyError:
        log.debug(f"Couldn't find description for ID: {api_response['id']}")
        description = None
    return description


def get_birth_date(api_response):
    try:
        birth_date = api_response["claims"]["P569"][0]["mainsnak"]["datavalue"][
            "value"
        ]["time"]
    except KeyError:
        log.debug(f"Couldn't find birth date for ID: {api_response['id']}")
        birth_date = None
    return birth_date


def get_death_date(api_response):
    try:
        death_date = api_response["claims"]["P570"][0]["mainsnak"]["datavalue"][
            "value"
        ]["time"]
    except KeyError:
        log.debug(f"Couldn't find death date for ID: {api_response['id']}")
        death_date = None
    return death_date


async def get_variants(api_response):
    try:
        aliases = [alias["value"] for alias in api_response["aliases"]["en"]]
    except KeyError:
        aliases = []

    try:
        same_as_elements = api_response["claims"]["P460"]
    except KeyError:
        same_as_elements = []

    same_as_ids = [
        element["mainsnak"]["datavalue"]["value"]["id"] for element in same_as_elements
    ]
    same_as_responses = await asyncio.gather(
        *[get_wikidata_api_response(id) for id in same_as_ids]
    )
    same_as = [get_title(response) for response in same_as_responses]

    variants = aliases + same_as
    if not variants:
        log.debug(f"Couldn't find variants for ID: {api_response['id']}")
        variants = []

    return variants


async def get_broader_concepts(api_response):
    start_time = time.time()
    try:
        instace_of = api_response["claims"]["P31"]
    except KeyError:
        instace_of = []
    try:
        subclass_of = api_response["claims"]["P279"]
    except KeyError:
        subclass_of = []

    concept_elements = instace_of + subclass_of
    if not concept_elements:
        log.debug(
            f"Couldn't find broader concepts for ID: {api_response['id']}")
        return None

    concept_ids = [
        element["mainsnak"]["datavalue"]["value"]["id"] for element in concept_elements
    ]

    responses = await asyncio.gather(
        *[get_wikidata_api_response(id) for id in concept_ids]
    )

    concepts = [get_title(response) for response in responses]

    log.debug(
        f'Got broader concepts for ID: {api_response["id"]}, '
        f"which took took {round(time.time() - start_time, 2)}s"
    )
    return concepts


async def get_wikidata_data(wikidata_id):
    api_response = await get_wikidata_api_response(wikidata_id)

    title = get_title(api_response)
    description = get_description(api_response)
    birth_date = get_birth_date(api_response)
    death_date = get_death_date(api_response)
    variants = await get_variants(api_response)
    broader_concepts = await get_broader_concepts(api_response)

    log.debug(f"Got data from wikidata for ID: {wikidata_id}")

    return {
        "id": wikidata_id,
        "title": title,
        "description": description,
        "birth_date": birth_date,
        "death_date": death_date,
        "variants": variants,
        "broader_concepts": broader_concepts,
    }
