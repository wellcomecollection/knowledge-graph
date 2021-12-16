from pathlib import Path

from . import clean, http_client


def get_lcsh_id_from_wikidata(wikidata):
    try:
        lcsh_id = wikidata["claims"]["P244"][0]["mainsnak"]["datavalue"][
            "value"
        ]
    except (KeyError, IndexError):
        lcsh_id = None
    return lcsh_id


def get_lcsh_data(lcsh_id):
    if lcsh_id.startswith("s"):
        url = f"http://id.loc.gov/authorities/subjects/{lcsh_id}.json"
    elif lcsh_id.startswith("n"):
        url = f"http://id.loc.gov/authorities/names/{lcsh_id}.json"
    else:
        raise ValueError(f"'{lcsh_id}' is not a valid library of congress ID")

    response = http_client.get(url)
    if response.status_code != 200:
        raise ValueError(f"'{lcsh_id}' is not a valid library of congress ID")

    for element in response.json():
        if element["@id"] == url.replace(".json", ""):
            return element


def get_lcsh_variant_names(lcsh_data):
    key = "http://www.w3.org/2004/02/skos/core#altLabel"
    if key in lcsh_data:
        variants = [clean(label["@value"]) for label in lcsh_data[key]]
    else:
        variants = []
    return variants


def get_lcsh_preferred_name(lcsh_data):
    key = "http://www.w3.org/2004/02/skos/core#prefLabel"
    if key in lcsh_data:
        preferred_name = clean(lcsh_data[key][0]["@value"])
    else:
        preferred_name = ""
    return preferred_name


def get_wikidata_id_from_lcsh_data(lcsh_data):
    wikidata_id = None
    keys = [
        "http://www.w3.org/2004/02/skos/core#exactMatch",
        "http://www.w3.org/2004/02/skos/core#closeMatch",
        "http://www.loc.gov/mads/rdf/v1#hasCloseExternalAuthority",
    ]
    for key in keys:
        if key in lcsh_data:
            for entry in lcsh_data[key]:
                if entry["@id"].startswith("http://www.wikidata.org/entity/"):
                    wikidata_id = Path(entry["@id"]).name
                    break
    return wikidata_id
