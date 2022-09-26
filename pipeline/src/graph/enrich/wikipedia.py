from . import clean, fetch_json


def get_wikipedia_label_from_wikidata(wikidata):
    try:
        wikipedia_label = wikidata["sitelinks"]["enwiki"]["title"]
    except (IndexError, KeyError, TypeError):
        wikipedia_label = None
    return wikipedia_label


def get_wikipedia_data(wikipedia_label):
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "prop": "|".join(["pageprops", "pageterms", "categories"]),
        "format": "json",
        "titles": wikipedia_label,
        "cllimit": 500,
        "clshow": "!hidden",
    }
    try:
        response = fetch_json(url, params)
        return list(response["query"]["pages"].values())[0]
    except Exception:
        raise ValueError(f"'{wikipedia_label}' is not a valid label")


def get_wikipedia_variant_labels(wikipedia_data):
    variants = []
    try:
        variants.extend(wikipedia_data["terms"]["alias"])
    except (KeyError, TypeError):
        pass
    try:
        variants.append(wikipedia_data["pageprops"]["label"])
    except (KeyError, TypeError):
        pass
    try:
        variants.append(wikipedia_data["terms"]["label"])
    except (KeyError, TypeError):
        pass
    return variants


def get_wikipedia_preferred_label(wikipedia_data):
    try:
        preferred_label = clean(wikipedia_data["title"])
    except (KeyError, TypeError):
        preferred_label = ""
    return preferred_label


def get_wikipedia_description(wikipedia_data):
    description = ""
    try:
        description = wikipedia_data["terms"]["description"][0]
    except (KeyError, TypeError):
        pass
    try:
        description = wikipedia_data["pageprops"]["wikibase-shortdesc"][0]
    except (KeyError, TypeError):
        pass
    return description


def get_wikidata_id_from_wikipedia_data(wikipedia_data):
    try:
        wikidata_id = wikipedia_data["pageprops"]["wikibase_item"]
    except (KeyError, TypeError):
        wikidata_id = ""
    return wikidata_id
