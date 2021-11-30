from time import sleep
import os

from neomodel import config, db
from neomodel.util import clear_neo4j_database


def get_neo4j_session(clean=True):
    print("Connecting to neo4j...")

    # test the connection to neo4j
    while True:
        try:
            db.cypher_query("MATCH (n) RETURN n LIMIT 1")
            break
        except:
            print("Waiting for neo4j to be live...")
            sleep(1)
            continue

    config.DATABASE_URL = os.environ["NEO4J_BOLT_URL"]
    db.set_connection(os.environ["NEO4J_BOLT_URL"])
    if clean:
        clear_neo4j_database(db)
    return db

