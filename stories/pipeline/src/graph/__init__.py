import os
from time import sleep

from neo4j.exceptions import ServiceUnavailable
from neomodel import config, db
from neomodel.util import clear_neo4j_database
from structlog import get_logger

log = get_logger()


def get_neo4j_session(clean=True):
    config.DATABASE_URL = os.environ["NEO4J_BOLT_URL"]
    db.set_connection(os.environ["NEO4J_BOLT_URL"])
    wait_until_neo4j_is_live()
    if clean:
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
