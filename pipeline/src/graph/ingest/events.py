from dateutil.parser import parse

from . import Event, get_logger
from .decorators import handle_neo4j_session_timeout

log = get_logger(__name__)


@handle_neo4j_session_timeout
def ingest_event(event):
    """
    Add a new event node to the graph.
    """
    try:
        description = event["promo"][0]["primary"]["caption"][0]["text"]
    except (KeyError, IndexError, TypeError):
        description = ""
    try:
        image_url = event["promo"][0]["primary"]["image"]["url"]
    except (KeyError, IndexError, TypeError):
        image_url = ""
    try:
        image_alt = event["promo"][0]["primary"]["image"]["alt"]
    except (KeyError, IndexError, TypeError):
        image_alt = ""
    try:
        location = event["locations"][0]["location"]["slug"]
    except (KeyError, IndexError, TypeError):
        location = ""
    try:
        format = event["format"]["slug"]
    except (KeyError, IndexError, TypeError):
        format = ""

    event_data = {
        "title": event["title"][0]["text"],
        "format": format,
        "description": description,
        "start_date": parse(event["times"][0]["startDateTime"]).date(),
        "end_date": parse(event["times"][0]["endDateTime"]).date(),
        "image_url": image_url,
        "image_alt": image_alt,
        "location": location,
    }

    existing_event = Event.nodes.first_or_none(**event_data)
    if existing_event:
        log.debug("Found existing event", uid=existing_event.uid)
    else:
        log.debug("Creating event", title=event["title"][0]["text"])
        Event(**event_data).save()
