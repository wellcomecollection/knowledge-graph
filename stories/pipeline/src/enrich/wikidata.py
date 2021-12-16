from httpx import ConnectError

from . import clean, http_client


def get_wikidata_id(concept_name):
    response = http_client.get(
        "https://www.wikidata.org/w/api.php",
        params={
            "action": "wbsearchentities",
            "language": "en",
            "format": "json",
            "search": concept_name,
        },
    ).json()

    # naively select the first result
    try:
        wikidata_id = response["search"][0]["id"]
    except IndexError:
        wikidata_id = None
    return wikidata_id


def get_wikidata(wikidata_id):
    response = http_client.get(
        f"http://www.wikidata.org/wiki/Special:EntityData/{wikidata_id}.json"
    ).json()
    return response["entities"][wikidata_id]


def get_wikidata_preferred_name(wikidata):
    try:
        preferred_name = clean(wikidata["labels"]["en"]["value"])
    except (IndexError, KeyError, ConnectError):
        preferred_name = ''
    return preferred_name


def get_wikidata_variant_names(
    wikidata, languages=["en", "en-gb", "en-ca", "en-us", "en-simple"]
):
    try:
        labels = [
            label["value"]
            for label in wikidata["labels"].values()
            if label["language"] in languages
        ]
        aliases = [
            alias["value"]
            for group in wikidata["aliases"].values()
            for alias in group
            if alias["language"] in languages
        ]
        variant_names = list(set([clean(name) for name in labels + aliases]))

    except (IndexError, KeyError, ConnectError):
        variant_names = []

    return variant_names


def get_wikidata_description(wikidata):
    try:
        description = wikidata["descriptions"]["en"]["value"]

    except (IndexError, KeyError, ConnectError):
        description = ""

    return description


def get_contributor_wikidata_ids(wikidata):
    try:
        contributors = [
            author["mainsnak"]["datavalue"]["value"]["id"]
            for author in wikidata["claims"]["P50"]
        ]
    except (IndexError, KeyError, ConnectError):
        contributors = []
    return contributors
