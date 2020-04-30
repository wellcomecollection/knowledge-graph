import requests
import logging

log = logging.getLogger(__name__)


def get_wikidata_api_response(wikidata_id):
    wikidata_url = f'http://www.wikidata.org/wiki/Special:EntityData/{wikidata_id}.json'
    wikidata_response = requests.get(wikidata_url).json()
    api_response = wikidata_response['entities'][wikidata_id]
    return api_response


def get_wikidata_data(wikidata_id):
    api_response = get_wikidata_api_response(wikidata_id)

    try:
        label = api_response['labels']['en']['value']
    except KeyError:
        log.info(f'Couldn\'t find label for ID: {wikidata_id}')
        label = None

    try:
        description = api_response['descriptions']['en']['value']
    except KeyError:
        log.info(f'Couldn\'t find description for ID: {wikidata_id}')
        description = None

    try:
        aliases = [
            alias['value'] for alias in api_response['aliases']['en']
        ]
    except KeyError:
        log.info(f'Couldn\'t find aliases for ID: {wikidata_id}')
        aliases = []

    try:
        birth_date = api_response['claims']['P569'][0]['mainsnak']['datavalue']['value']['time']
    except KeyError:
        log.info(f'Couldn\'t find birth date for ID: {wikidata_id}')
        birth_date = None

    try:
        death_date = api_response['claims']['P570'][0]['mainsnak']['datavalue']['value']['time']
    except KeyError:
        log.info(f'Couldn\'t find death date for ID: {wikidata_id}')
        death_date = None

    return {
        'id': wikidata_id,
        'title': label,
        'description': description,
        'birth_date': birth_date,
        'death_date': death_date,
        'variants': aliases
    }
