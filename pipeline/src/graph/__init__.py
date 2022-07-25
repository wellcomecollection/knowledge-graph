import os
from time import sleep

from neo4j.exceptions import ServiceUnavailable
from neomodel import config, db
from neomodel.util import clear_neo4j_database

from ..enrich.loc import (
    get_loc_data,
    get_loc_id_from_wikidata,
    get_loc_preferred_label,
    get_loc_variant_labels,
    get_wikidata_id_from_loc_data,
)
from ..enrich.mesh import (
    get_mesh_data,
    get_mesh_description,
    get_mesh_id_from_wikidata,
    get_mesh_preferred_concept_data,
    get_mesh_preferred_label,
)
from ..enrich.wikidata import (
    get_wikidata,
    get_wikidata_description,
    get_wikidata_id,
    get_wikidata_preferred_label,
    get_wikidata_variant_labels,
)
from ..utils import get_logger

log = get_logger(__name__)


def get_neo4j_session(clear=False):
    config.DATABASE_URL = os.environ["NEO4J_CONNECTION_URI"]
    db.set_connection(os.environ["NEO4J_CONNECTION_URI"])
    wait_until_neo4j_is_live()
    if clear:
        log.info("Clearing neo4j database")
        clear_neo4j_database(db)
    return db


def wait_until_neo4j_is_live():
    while True:
        try:
            db.cypher_query("MATCH (n) RETURN n LIMIT 1")
            break
        except ServiceUnavailable:
            sleep(1)
            log.info("Connecting to neo4j...")
