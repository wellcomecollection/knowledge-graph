from .utils import fetch_json


def get_prismic_master_ref():
    response = fetch_json("https://wellcomecollection.cdn.prismic.io/api")
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


def get_fulltext(slices):
    paragraphs = [
        paragraph["text"]
        for slice in slices
        if slice["slice_type"] == "text"
        for paragraph in slice["primary"]["text"]
    ]
    return "\n".join(paragraphs)


def get_standfirst(slices):
    paragraphs = [
        paragraph["text"]
        for slice in slices
        if slice["slice_type"] == "standfirst"
        for paragraph in slice["primary"]["text"]
    ]
    return "\n".join(paragraphs)


def yield_exhibitions(size=None):
    response = httpx.get(
        "https://wellcomecollection.cdn.prismic.io/api/v2/documents/search",
        params={
            "ref": master_ref,
            "q": '[[at(document.type, "exhibitions")]]',
            "pageSize": size,
        },
    )
    for result in response["results"]:
        yield result["data"]


def yield_events(size=None):
    response = fetch_json(
        "https://wellcomecollection.cdn.prismic.io/api/v2/documents/search",
        params={
            "ref": master_ref,
            "q": '[[at(document.type, "events")]]',
            "pageSize": size,
        },
    )
    for result in response["results"]:
        yield result["data"]
