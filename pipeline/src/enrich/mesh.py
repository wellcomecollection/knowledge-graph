from pathlib import Path

from . import clean, fetch_json


def get_mesh_id_from_wikidata(wikidata):
    try:
        mesh_id = wikidata["claims"]["P486"][0]["mainsnak"]["datavalue"][
            "value"
        ]
    except (IndexError, KeyError, TypeError):
        mesh_id = None
    return mesh_id


def get_mesh_data(mesh_id):
    try:
        response = fetch_json(f"https://id.nlm.nih.gov/mesh/{mesh_id}.json")
    except Exception:
        raise ValueError(f"'{mesh_id}' is not a valid MeSH ID")
    return response


def get_mesh_preferred_concept_data(mesh_data):
    try:
        preferred_concept_id = Path(mesh_data["preferredConcept"]).name
        preferred_concept_data = get_mesh_data(preferred_concept_id)
    except (KeyError, IndexError, ValueError, TypeError):
        preferred_concept_data = mesh_data
    return preferred_concept_data


def get_mesh_preferred_name(mesh_data):
    try:
        preferred_name = clean(mesh_data["label"]["@value"])
    except (KeyError, TypeError):
        preferred_name = ""
    return preferred_name


def get_mesh_description(mesh_data):
    try:
        description = mesh_data["scopeNote"]["@value"]
    except (KeyError, TypeError):
        description = ""
    return description
