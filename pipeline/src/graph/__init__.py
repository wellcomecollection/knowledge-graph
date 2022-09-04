import os
from time import sleep

from neo4j.exceptions import ServiceUnavailable
from neomodel import config, db, install_all_labels
from neomodel.util import clear_neo4j_database

from ..utils import clean, clean_csv, get_logger
from .enrich import (
    get_contributor_wikidata_ids,
    get_loc_data,
    get_loc_id_from_wikidata,
    get_loc_preferred_label,
    get_loc_variant_labels,
    get_mesh_data,
    get_mesh_description,
    get_mesh_id_from_wikidata,
    get_mesh_preferred_concept_data,
    get_mesh_preferred_label,
    get_wikidata,
    get_wikidata_description,
    get_wikidata_id,
    get_wikidata_id_from_loc_data,
    get_wikidata_preferred_label,
    get_wikidata_variant_labels,
    get_wikipedia_data,
)
from .ingest import ingest_event, ingest_exhibition, ingest_story, ingest_work
from .models import (
    Concept,
    Event,
    Exhibition,
    Person,
    SourceConcept,
    SourceType,
    Work,
)
from .neighbours import (
    get_loc_neighbours,
    get_mesh_neighbours,
    get_wikidata_neighbours,
    get_wikipedia_neighbours,
)
from .sources import (
    connect_label_derived_source,
    connect_loc_source,
    connect_mesh_source,
    connect_wikidata_source,
    connect_wikipedia_source,
)

log = get_logger(__name__)


def get_neo4j_session(clear=False):
    config.AUTO_INSTALL_LABELS = True
    config.DATABASE_URL = os.environ["NEO4J_CONNECTION_URI"]
    db.set_connection(os.environ["NEO4J_CONNECTION_URI"])
    wait_until_neo4j_is_live()
    if clear:
        log.info("Clearing neo4j database")
        clear_neo4j_database(db)
    install_all_labels()
    return db


def wait_until_neo4j_is_live():
    while True:
        try:
            db.cypher_query("MATCH (n) RETURN n LIMIT 1")
            break
        except ServiceUnavailable:
            sleep(1)
            log.info("Connecting to neo4j...")
