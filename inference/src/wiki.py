import requests
from urllib.parse import quote

# wiki.py
base_wiki_url = 'https://en.wikipedia.org/w/api.php'


def get_wikidata_candidates(query):
    wikipedia_search_params = {
        'action': 'query',
        'format': 'json',
        'list': 'search',
        'srsearch': query,
    }

    wikipedia_response = requests.get(
        url=base_wiki_url, params=wikipedia_search_params
    ).json()

    candidate_titles = [
        hit['title']for hit in wikipedia_response['query']['search']
    ]
    candidates = {text.lower(): text for text in candidate_titles}
    return candidates


def get_wikidata_id(wikidata_title):
    wikidata_search_params = {
        'action': 'query',
        'format': 'json',
        'prop': 'pageprops',
        'ppprop': 'wikibase_item',
        'titles': quote(wikidata_title),
    }

    wikidata_response = requests.get(
        url=base_wiki_url, params=wikidata_search_params
    ).json()

    pages = wikidata_response['query']['pages']
    unpacked_page = list(pages.values())[0]

    wikidata_id = unpacked_page['pageprops']['wikibase_item']
    return wikidata_id
