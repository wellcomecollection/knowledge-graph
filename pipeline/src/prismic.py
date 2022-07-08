from .utils import fetch_json


def get_prismic_master_ref():
    response = fetch_json("https://wellcomecollection.cdn.prismic.io/api")
    return response["refs"][0]["ref"]


master_ref = get_prismic_master_ref()


def get_story_data(id, ref=master_ref):
    try:
        response = fetch_json(
            "https://wellcomecollection.cdn.prismic.io/api/v2/documents/search",
            params={"ref": ref, "q": f'[[at(document.id, "{id}")]]'},
        )
        story_data = response["results"][0]["data"]
    except (KeyError, IndexError, TypeError, ValueError):
        story_data = {"body": []}
    return story_data


def get_story_fulltext(story_data):
    paragraphs = [
        paragraph["text"]
        for slice in story_data["body"]
        if slice["slice_type"] == "text"
        for paragraph in slice["primary"]["text"]
    ]
    return "\n".join(paragraphs)


def get_story_standfirst(story_data):
    paragraphs = [
        paragraph["text"]
        for slice in story_data["body"]
        if slice["slice_type"] == "standfirst"
        for paragraph in slice["primary"]["text"]
    ]
    return "\n".join(paragraphs)


def get_story_image(story_data):
    try:
        image_url = story_data["promo"][0]["primary"]["image"]["url"]
    except (KeyError, IndexError, TypeError, ValueError):
        image_url = None
    return image_url


def yield_exhibitions(size=100):
    response = fetch_json(
        "https://wellcomecollection.cdn.prismic.io/api/v2/documents/search",
        params={
            "ref": master_ref,
            "q": '[[at(document.type, "exhibitions")]]',
            "pageSize": size,
        },
    )
    for result in response["results"]:
        yield result["data"]


def yield_events(size=100):
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
