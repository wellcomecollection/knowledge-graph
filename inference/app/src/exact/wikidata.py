import requests
import logging

log = logging.getLogger(__name__)


def get_wikidata_data(wikidata_id):
    wikidata_url = f'http://www.wikidata.org/wiki/Special:EntityData/{wikidata_id}.json'
    wikidata_response = requests.get(wikidata_url).json()
    wikidata_id = list(wikidata_response['entities'].keys())[0]
    wikidata_record = wikidata_response['entities'][wikidata_id]

    try:
        label = wikidata_record['labels']['en']['value']
    except KeyError:
        log.info(f'Couldn\'t find label for ID: {wikidata_id}')
        label = None

    try:
        description = wikidata_record['descriptions']['en']['value']
    except KeyError:
        log.info(f'Couldn\'t find description for ID: {wikidata_id}')
        description = None

    try:
        aliases = [
            alias['value'] for alias in wikidata_record['aliases']['en']
        ]
    except KeyError:
        log.info(f'Couldn\'t find aliases for ID: {wikidata_id}')
        aliases = []

    try:
        birth_date = wikidata_record['claims']['P569'][0]['mainsnak']['datavalue']['value']['time']
    except KeyError:
        log.info(f'Couldn\'t find birth date for ID: {wikidata_id}')
        birth_date = None

    try:
        death_date = wikidata_record['claims']['P570'][0]['mainsnak']['datavalue']['value']['time']
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
