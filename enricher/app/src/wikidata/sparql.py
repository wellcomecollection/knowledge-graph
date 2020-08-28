from pathlib import Path

from weco_datascience.http import fetch_url_json
from weco_datascience.logging import get_logger

log = get_logger(__name__)


async def get_wikidata_sparql_response(query):
    response = await fetch_url_json(
        url="https://query.wikidata.org/sparql",
        params={"query": query, "format": "json"},
    )
    response = [item["q"] for item in response.json()["results"]["bindings"]]
    return response


async def get_wikidata_id_from_prop(prop_id, value):
    query = (
        "SELECT DISTINCT ?q "
        f"""{{ VALUES ?value {{ "{value}" }} . """
        f"?q wdt:{prop_id} ?value }}"
    )
    response = await get_wikidata_sparql_response(query)
    wikidata_id = Path(response[0]["value"]).name
    return wikidata_id
