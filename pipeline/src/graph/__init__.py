import os
from time import sleep

from neo4j.exceptions import ServiceUnavailable
from neomodel import config, db
from neomodel.util import clear_neo4j_database
from structlog import get_logger

from ..enrich.lcsh import (
    get_lcsh_data,
    get_lcsh_id_from_wikidata,
    get_lcsh_preferred_name,
    get_lcsh_variant_names,
    get_wikidata_id_from_lcsh_data,
)
from ..enrich.mesh import (
    get_mesh_data,
    get_mesh_description,
    get_mesh_id_from_wikidata,
    get_mesh_preferred_concept_data,
    get_mesh_preferred_name,
)
from ..enrich.wikidata import (
    get_wikidata,
    get_wikidata_description,
    get_wikidata_id,
    get_wikidata_preferred_name,
    get_wikidata_variant_names,
)

log = get_logger()


def get_neo4j_session(clear=True):
    config.DATABASE_URL = os.environ["NEO4J_BOLT_URL"]
    db.set_connection(os.environ["NEO4J_BOLT_URL"])
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
            log.info("Waiting for Neo4j to start...")
            sleep(5)