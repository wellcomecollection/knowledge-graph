import httpx


def get_lcsh_id(wikidata):
    try:
        lcsh_id = wikidata["claims"]["P244"][0]["mainsnak"]["datavalue"][
            "value"
        ]
    except (KeyError, IndexError):
        lcsh_id = None
    return lcsh_id


def get_lcsh_data(lcsh_id):
    url = f"http://id.loc.gov/authorities/subjects/{lcsh_id}.json"

    try:
        response = httpx.get(url)
    except ValueError as e:
        raise e
    if response.status_code == 200:
        pass
    elif response.status_code == 404:
        raise ValueError(f"{lcsh_id} is not a valid library of congress ID")
    else:
        raise ValueError(
            f"something unexpected happened when calling url: {url}"
        )

    for element in response.json():
        if element["@id"] == url.replace(".json", ""):
            return element


def get_lcsh_variant_names(lcsh_data):
    key = "http://www.w3.org/2004/02/skos/core#altLabel"
    if key in lcsh_data:
        variants = [label["@value"] for label in lcsh_data[key]]
    else:
        variants = []
    return variants


def get_lcsh_preferred_name(lcsh_data):
    key = "http://www.w3.org/2004/02/skos/core#prefLabel"
    if key in lcsh_data:
        preferred_name = lcsh_data[key][0]["@value"]
    else:
        preferred_name = None
    return preferred_name
