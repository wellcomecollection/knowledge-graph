from . import clean, fetch_json


def get_wikipedia_label_from_wikidata(wikidata):
    try:
        wikipedia_label = wikidata["claims"]["sitelinks"]["enwiki"]["name"]
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
        data = list(response["query"]["pages"].values())[0]
        return data
    except Exception:
        raise ValueError(f"'{wikipedia_label}' is not a valid label")


def get_wikipedia_neighbours(wikipedia_data):
    page_labels = [
        category_label["title"].replace("Category:", "")
        for category_label in wikipedia_data["categories"]
    ]
    return page_labels


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
    return variants


def get_wikipedia_preferred_label(wikipedia_data):
    try:
        preferred_label = clean(wikipedia_data["title"])
    except (KeyError, TypeError):
        preferred_label = ""
    return preferred_label


def get_wikipedia_descriptions(wikipedia_data):
    descriptions = []
    try:
        descriptions.extend(wikipedia_data["terms"]["description"])
    except (KeyError, TypeError):
        pass
    try:
        descriptions.append(wikipedia_data["pageprops"]["wikibase-shortdesc"])
    except (KeyError, TypeError):
        pass
    return descriptions
