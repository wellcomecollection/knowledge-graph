from pathlib import Path

from . import clean, http_client


def get_mesh_id_from_wikidata(wikidata):
    try:
        mesh_id = wikidata["claims"]["P486"][0]["mainsnak"]["datavalue"][
            "value"
        ]
    except (KeyError, IndexError):
        mesh_id = None
    return mesh_id


def get_mesh_data(mesh_id):
    response = http_client.get(f"https://id.nlm.nih.gov/mesh/{mesh_id}.json")
    if response.status_code == 200:
        mesh_data = response.json()
    else:
        raise ValueError(f"'{mesh_id}' is not a valid MeSH ID")
    return mesh_data


def get_mesh_preferred_concept_data(mesh_data):
    try:
        preferred_concept_id = Path(mesh_data["preferredConcept"]).name
        preferred_concept_data = get_mesh_data(preferred_concept_id)
    except (KeyError, ValueError):
        preferred_concept_data = mesh_data
    return preferred_concept_data


def get_mesh_preferred_name(mesh_data):
    try:
        preferred_name = clean(mesh_data["label"]["@value"])
    except KeyError:
        preferred_name = ""
    return preferred_name


def get_mesh_description(mesh_data):
    try:
        description = mesh_data["scopeNote"]["@value"]
    except KeyError:
        description = ""
    return description
