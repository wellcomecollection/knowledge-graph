import httpx


def get_mesh_id(wikidata):
    try:
        mesh_id = wikidata["claims"]["P486"][0]["mainsnak"]["datavalue"][
            "value"
        ]
    except (KeyError, IndexError):
        mesh_id = None
    return mesh_id


def get_mesh_data(mesh_id):
    response = httpx.get(
        url="https://meshb.nlm.nih.gov/api/search/record",
        params={
            "searchInField": "ui",
            "sort": "",
            "size": "1",
            "searchType": "exactMatch",
            "searchMethod": "FullWord",
            "q": mesh_id,
        },
    )
    try:
        mesh_data = response.json()["hits"]["hits"][0]["_source"]["_generated"]
    except IndexError:
        raise ValueError(f"{mesh_id} is not a valid MeSH ID")
    except KeyError:
        raise ValueError(
            f"something unexpected happened when calling url: {response.url}"
        )
    return mesh_data


def get_mesh_preferred_name(mesh_data):
    try:
        preferred_name = mesh_data["RecordName"]
    except KeyError:
        preferred_name = None
    return preferred_name


def get_mesh_description(mesh_data):
    if "PreferredConceptScopeNote" in mesh_data:
        description = mesh_data["PreferredConceptScopeNote"]
    elif "scrNote" in mesh_data:
        description = mesh_data["scrNote"]
    else:
        description = None
    return description


def get_mesh_variant_names(mesh_data):
    try:
        variants = (
            mesh_data["originalEntryTerms"] + mesh_data["permutatedEntryTerms"]
        )
    except KeyError:
        variants = []
    return variants
