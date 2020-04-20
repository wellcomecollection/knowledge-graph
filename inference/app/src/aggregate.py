import logging

from .exact.lc_names import get_lc_names_data
from .exact.utils import lc_names_id_to_wikidata_id
from .exact.wikidata import get_wikidata_data

log = logging.getLogger(__name__)


def aggregate_lc_names_data(lc_names_id):
    lc_names_data = get_lc_names_data(lc_names_id)
    log.info(f"Got lc_names data from lc_names for ID: {lc_names_id}")
    try:
        wikidata_id = lc_names_id_to_wikidata_id(lc_names_id)
        log.info(
            f'Found a link from lc_names ID: {lc_names_id} to wikidata ID: {wikidata_id}'
        )

        wikidata_data = get_wikidata_data(wikidata_id)
        log.info(f"Got lc_names data from wikidata for ID: {lc_names_id}")
    except ValueError:
        log.info(
            f"Couldn't find a wikidata record for lc_names ID: {lc_names_id}"
        )
        wikidata_data = {}

    return {
        "exact": {
            "lc_names": lc_names_data,
            "wikidata": wikidata_data
        },
        "inferred": {}  # TODO
    }