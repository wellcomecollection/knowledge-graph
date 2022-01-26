from httpx import ConnectError, RemoteProtocolError

from . import clean, fetch_json


def get_wikidata_id(concept_name):
    response = fetch_json(
        "https://www.wikidata.org/w/api.php",
        params={
            "action": "wbsearchentities",
            "language": "en",
            "format": "json",
            "search": concept_name,
        },
    )

    # naively select the first result
    try:
        wikidata_id = response["search"][0]["id"]
    except (IndexError, KeyError, TypeError):
        wikidata_id = None
    return wikidata_id


def get_wikidata(wikidata_id):
    try:
        response = fetch_json(
            f"http://www.wikidata.org/wiki/Special:EntityData/{wikidata_id}.json"
        )
        return response["entities"][wikidata_id]
    except (KeyError, IndexError, ConnectError, RemoteProtocolError):
        return None


def get_wikidata_preferred_name(wikidata):
    try:
        preferred_name = clean(wikidata["labels"]["en"]["value"])
    except (IndexError, KeyError, TypeError):
        preferred_name = ""
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

    except (IndexError, KeyError, TypeError):
        variant_names = []

    return variant_names


def get_wikidata_description(wikidata):
    try:
        description = wikidata["descriptions"]["en"]["value"]

    except (IndexError, KeyError, TypeError):
        description = ""

    return description


def get_contributor_wikidata_ids(wikidata):
    try:
        contributors = []
        if "P50" in wikidata["claims"]:
            contributors.extend(
                [
                    author["mainsnak"]["datavalue"]["value"]["id"]
                    for author in wikidata["claims"]["P50"]
                ]
            )
        if "P110" in wikidata["claims"]:
            contributors.extend(
                [
                    illustrator["mainsnak"]["datavalue"]["value"]["id"]
                    for illustrator in wikidata["claims"]["P110"]
                ]
            )
    except (IndexError, KeyError, TypeError):
        contributors = []
    return contributors
