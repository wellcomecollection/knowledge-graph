import httpx
from httpx import ConnectError

from .utils import clean


def get_wikidata_id(concept_name):
    response = httpx.get(
        "https://www.wikidata.org/w/api.php",
        params={
            "action": "wbsearchentities",
            "language": "en",
            "format": "json",
            "search": concept_name,
        },
    ).json()

    # naively select the first result
    wikidata_id = response["search"][0]["id"]
    return wikidata_id


def get_variant_names(
    concept_name, languages=["en", "en-gb", "en-ca", "en-us", "en-simple"]
):
    try:
        wikidata_id = get_wikidata_id(concept_name)
        response = httpx.get(
            "http://www.wikidata.org/wiki/Special:EntityData/"
            f"{wikidata_id}.json"
        ).json()

        data = response["entities"][wikidata_id]
        labels = [
            label["value"]
            for label in data["labels"].values()
            if label["language"] in languages
        ]
        aliases = [
            alias["value"]
            for group in data["aliases"].values()
            for alias in group
            if alias["language"] in languages
        ]
        variant_names = list(set([clean(name) for name in labels + aliases]))

    except (IndexError, KeyError, ConnectError):
        variant_names = []

    return variant_names
