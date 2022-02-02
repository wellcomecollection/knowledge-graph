from pathlib import Path

from . import clean, fetch_json


def get_loc_id_from_wikidata(wikidata):
    try:
        loc_id = wikidata["claims"]["P244"][0]["mainsnak"]["datavalue"]["value"]
    except (KeyError, IndexError, TypeError):
        loc_id = None
    return loc_id


def get_loc_data(source_id):
    source_type = "subjects" if source_id.startswith("s") else "names"
    url = f"http://id.loc.gov/authorities/{source_type}/{source_id}.skos.json"
    try:
        response = fetch_json(url)
        key = url.replace(".skos.json", "")
        for element in response:
            if element["@id"] == key:
                return element
    except (KeyError, IndexError, ValueError, TypeError):
        raise ValueError(f"'{url}' is not a valid library of congress URL")


def get_loc_variant_names(loc_data):
    key = "http://www.w3.org/2004/02/skos/core#altLabel"
    if key in loc_data:
        variants = [clean(label["@value"]) for label in loc_data[key]]
    else:
        variants = []
    return variants


def get_loc_preferred_name(loc_data):
    key = "http://www.w3.org/2004/02/skos/core#prefLabel"
    if key in loc_data:
        preferred_name = clean(loc_data[key][0]["@value"])
    else:
        preferred_name = ""
    return preferred_name


def get_wikidata_id_from_loc_data(loc_data):
    wikidata_id = None
    keys = [
        "http://www.w3.org/2004/02/skos/core#exactMatch",
        "http://www.w3.org/2004/02/skos/core#closeMatch",
    ]
    for key in keys:
        if key in loc_data:
            for entry in loc_data[key]:
                if entry["@id"].startswith("http://www.wikidata.org/entity/"):
                    wikidata_id = Path(entry["@id"]).name
                    break
    return wikidata_id
