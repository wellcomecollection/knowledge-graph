import httpx


def get_slices(id):
    response = httpx.get(
        "https://wellcomecollection.cdn.prismic.io/api/v2/documents/search",
        params={"ref": "YZZ4mREAACcAWBme", "q": f'[[at(document.id, "{id}")]]'},
    ).json()
    slices = response["results"][0]["data"]["body"]
    return slices


def get_fulltext(id):
    slices = get_slices(id)
    paragraphs = [
        paragraph["text"]
        for slice in slices
        if slice["slice_type"] == "text"
        for paragraph in slice["primary"]["text"]
    ]
    return "\n".join(paragraphs)


def get_standfirst(id):
    slices = get_slices(id)
    paragraphs = [
        paragraph["text"]
        for slice in slices
        if slice["slice_type"] == "standfirst"
        for paragraph in slice["primary"]["text"]
    ]
    return "\n".join(paragraphs)
