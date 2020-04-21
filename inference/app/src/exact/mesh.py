import requests
import logging

log = logging.getLogger(__name__)


def get_mesh_api_response(mesh_id):
    url = "https://meshb.nlm.nih.gov/api/search/record"
    params = {
        "searchInField": "ui",
        "sort": "",
        "size": "1",
        "searchType": "exactMatch",
        "searchMethod": "FullWord",
        "q": mesh_id
    }
    response = requests.get(url, params)
    try:
        generated_response = (
            response.json()['hits']['hits'][0]['_source']['_generated']
        )
    except IndexError:
        raise ValueError(f'{mesh_id} is not a valid MeSH ID')
    except KeyError:
        requested_url = response.url
        raise ValueError(
            f"something unexpected happened when calling url: {requested_url}"
        )
    return generated_response


def get_mesh_data(mesh_id):
    api_response = get_mesh_api_response(mesh_id)

    try:
        preferred_name = api_response["RecordName"]
    except KeyError:
        log.info(f'Couldn\'t find preferred name for ID: {mesh_id}')
        preferred_name = None

    if "PreferredConceptScopeNote" in api_response:
        description = api_response["PreferredConceptScopeNote"]
    elif "scrNote" in api_response:
        description = api_response["scrNote"]
    else:
        log.info(f'Couldn\'t find description for ID: {mesh_id}')
        description = None

    try:
        variants = api_response["originalEntryTerms"]
    except KeyError:
        log.info(f'Couldn\'t find variants for ID: {mesh_id}')
        variants = []

    return {
        "id": mesh_id,
        "preferred_name": preferred_name,
        "description": description,
        "variants": variants
    }
