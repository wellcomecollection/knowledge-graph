from dateutil.parser import parse

from . import Exhibition, get_logger
from .decorators import handle_neo4j_session_timeout

log = get_logger(__name__)


@handle_neo4j_session_timeout
def ingest_exhibition(exhibition):
    """
    Add a new exhibition node to the graph.
    """
    try:
        description = exhibition["promo"][0]["primary"]["caption"][0]["text"]
    except (KeyError, IndexError, TypeError):
        description = ""
    try:
        image_url = exhibition["promo"][0]["primary"]["image"]["url"]
    except (KeyError, IndexError, TypeError):
        image_url = ""
    try:
        image_alt = exhibition["promo"][0]["primary"]["image"]["alt"]
    except (KeyError, IndexError, TypeError):
        image_alt = ""
    try:
        location = exhibition["place"]["slug"]
    except (KeyError, IndexError, TypeError):
        location = ""

    exhibition_data = {
        "title": exhibition["title"][0]["text"],
        "format": (
            "Permanent exhibition"
            if exhibition["isPermanent"]
            else "Exhibition"
        ),
        "description": description,
        "start_date": parse(exhibition["start"]).date(),
        "end_date": parse(exhibition["end"]).date(),
        "image_url": image_url,
        "image_alt": image_alt,
        "location": location,
    }

    existing_exhibition = Exhibition.nodes.first_or_none(**exhibition_data)
    if existing_exhibition:
        log.debug("Found existing exhibition", uid=existing_exhibition.uid)
    else:
        log.debug("Creating exhibition", title=exhibition["title"][0]["text"])
        Exhibition(**exhibition_data).save()
