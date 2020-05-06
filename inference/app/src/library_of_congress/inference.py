import logging
from os.path import basename, splitext
from urllib.parse import quote

from . import fetch_url_json

log = logging.getLogger(__name__)


async def search_loc(query, authority_type):
    valid_authority_types = ["names", "subjects"]
    if authority_type not in valid_authority_types:
        raise ValueError(
            f"authority type must be one of: {valid_authority_types}"
        )

    query_url = (
        f"http://id.loc.gov/search/?q={quote(query)}&format=json"
        f"&q=cs%3Ahttp%3A%2F%2Fid.loc.gov%2Fauthorities%2F{authority_type}"
    )
    api_response = await fetch_url_json(query_url)
    if api_response["object"].status != 200:
        raise ValueError(
            f"Couldn't find '{query}' in Library of Congress {authority_type}"
        )

    try:
        loc_id = get_id_from_api_response(api_response["json"])
    except (ValueError, KeyError, IndexError):
        raise ValueError(
            f"Couldn't find '{query}' in Library of Congress {authority_type}"
        )
    log.info(f"Matched query: '{query}' to lc-{authority_type} ID: {loc_id}")
    return loc_id


def search_lc_names(query):
    lc_names_id = search_loc(query, authority_type="names")
    return lc_names_id


def search_lc_subjects(query):
    lc_subjects_id = search_loc(query, authority_type="subjects")
    return lc_subjects_id


def get_id_from_api_response(api_response):
    loc_id = None
    for element in api_response:
        if type(element) == list:
            if element[0] == "atom:entry":
                for subelement in element:
                    if type(subelement) == list:
                        if subelement[0] == "atom:link":
                            loc_url = subelement[1]["href"]
                            loc_id = get_id_from_loc_url(loc_url)
                            break
                # we're only interested in the top result, so we stop
                # traversing the response ASAP
                break

    if not loc_id:
        raise ValueError
    return loc_id


def get_id_from_loc_url(loc_url):
    return splitext(basename(loc_url))[0]
