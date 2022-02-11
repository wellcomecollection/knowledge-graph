from .utils import fetch_json


def get_work_data(id):
    try:
        data = fetch_json(
            f"https://api.wellcomecollection.org/catalogue/v2/works/{id}",
            params={"include": "subjects,notes,genres"},
        )
    except (KeyError, IndexError, TypeError, ValueError):
        data = {}
    return data


def get_description(work_data):
    try:
        description = work_data["description"]
    except (KeyError, IndexError, TypeError, ValueError):
        description = ""
    return description


def get_notes(work_data):
    try:
        notes = "\n".join([note["contents"] for note in work_data["notes"]])
    except (KeyError, IndexError, TypeError, ValueError):
        notes = ""
    return notes
