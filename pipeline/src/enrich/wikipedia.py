from . import clean, fetch_json


def get_wikipedia_name_from_wikidata(wikidata):
    try:
        wikipedia_name = wikidata["claims"]["sitelinks"]['enwiki']['name']
    except (IndexError, KeyError, TypeError):
        wikipedia_name = None
    return wikipedia_name


def get_wikipedia_data(wikipedia_name):
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "prop": "|".join(["pageprops", "pageterms", "categories"]),
        "format": "json",
        "titles": wikipedia_name,
        "cllimit": 500,
        "clshow": "!hidden",
    }
    try:
        response = fetch_json(url, params)
        data = list(response["query"]["pages"].values())[0]
        return data
    except Exception:
        raise ValueError(f"'{wikipedia_name}' is not a valid name")


def get_wikipedia_neighbours(wikipedia_data):
    page_names = [
        category_name['title'].replace("Category:", "")
        for category_name in wikipedia_data["categories"]
    ]
    return page_names


def get_wikipedia_variant_names(wikipedia_data):
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


def get_wikipedia_preferred_name(wikipedia_data):
    try:
        preferred_name = clean(wikipedia_data["title"])
    except (KeyError, TypeError):
        preferred_name = ""
    return preferred_name


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
