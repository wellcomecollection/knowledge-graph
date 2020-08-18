from .http import fetch_url_json
from .logging import get_logger

log = get_logger(__name__)


async def get_mesh_api_response(mesh_id):
    url = "https://meshb.nlm.nih.gov/api/search/record"
    params = {
        "searchInField": "ui",
        "sort": "",
        "size": "1",
        "searchType": "exactMatch",
        "searchMethod": "FullWord",
        "q": mesh_id
    }
    response = await fetch_url_json(url, params)
    try:
        generated_response = (
            response["json"]['hits']['hits'][0]['_source']['_generated']
        )
    except IndexError:
        raise ValueError(f'{mesh_id} is not a valid MeSH ID')
    except KeyError:
        requested_url = response["object"].url
        raise ValueError(
            f"something unexpected happened when calling url: {requested_url}"
        )
    return generated_response


def get_label(api_response):
    try:
        label = api_response["RecordName"]
    except KeyError:
        log.info(f"Couldn't find label for ID: {api_response['RecordUI']}")
        label = None
    return label


def get_description(api_response):
    if "PreferredConceptScopeNote" in api_response:
        description = api_response["PreferredConceptScopeNote"]
    elif "scrNote" in api_response:
        description = api_response["scrNote"]
    else:
        log.info(
            f"Couldn't find description for ID: {api_response['RecordUI']}"
        )
        description = None
    return description


def get_variants(api_response):
    try:
        variants = api_response["originalEntryTerms"]
    except KeyError:
        log.info(f"Couldn't find variants for ID: {api_response['RecordUI']}")
        variants = []
    return variants


async def get_mesh_data(mesh_id):
    api_response = await get_mesh_api_response(mesh_id)
    label = get_label(api_response)
    description = get_description(api_response)
    variants = get_variants(api_response)

    log.info(f"Got data from MeSH for ID: {mesh_id}")

    return {
        "id": mesh_id,
        "label": label,
        "description": description,
        "variants": variants
    }
