from .utils import fetch_json


def get_prismic_master_ref():
    response = fetch_json(
        "https://wellcomecollection.cdn.prismic.io/api",
    )
    return response["refs"][0]["ref"]


master_ref = get_prismic_master_ref()


def get_slices(id, ref=master_ref):
    try:
        response = fetch_json(
            "https://wellcomecollection.cdn.prismic.io/api/v2/documents/search",
            params={"ref": ref, "q": f'[[at(document.id, "{id}")]]'},
        )
        slices = response["results"][0]["data"]["body"]
    except (KeyError, IndexError, TypeError, ValueError):
        slices = []
    return slices


def get_fulltext(id):
    paragraphs = [
        paragraph["text"]
        for slice in get_slices(id)
        if slice["slice_type"] == "text"
        for paragraph in slice["primary"]["text"]
    ]
    return "\n".join(paragraphs)


def get_standfirst(id):
    paragraphs = [
        paragraph["text"]
        for slice in get_slices(id)
        if slice["slice_type"] == "standfirst"
        for paragraph in slice["primary"]["text"]
    ]
    return "\n".join(paragraphs)
