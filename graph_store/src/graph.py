import json
import logging
import os

from neo4j import GraphDatabase, basic_auth
from pypher import Pypher, __

from .credentials import get_secrets
from .enrich import enrich
from .logging import get_logger

log = get_logger(__name__)


class Graph:
    """
    Tidy interface to neo4j aura instance
    """

    def __init__(self):
        log.info("Initialising graph client")
        secrets = get_secrets("neo4j/credentials")

        self.driver = GraphDatabase.driver(
            uri=secrets["connection_uri"].replace("neo4j+s", "bolt+routing"),
            auth=basic_auth(
                user=secrets["username"],
                password=secrets["password"]
            )
        )
        log.info("Successfully initialised graph client")

    @staticmethod
    def _build_query_string(query):
        """
        Turn a pypher command into a usable query string by unpacking its bound
        params etc.
        """
        query_string = str(query)
        if query.bound_params:
            for key, value in query.bound_params.items():
                key = "$" + key
                value = "\"" + value.replace('"', '\\"') + "\""
                query_string = query_string.replace(key, value)
        return query_string

    def _run_command(self, query):
        """
        Run a query without expecting a response.
        eg. adding a node or edge to the graph
        """
        query_string = self._build_query_string(query)
        with self.driver.session() as session:
            session.run(query_string)

    def _run_query(self, query):
        """
        Run a query, expecting a response.
        eg. counting the nodes in the graph
        """
        query_string = self._build_query_string(query)

        def _query_fn(transaction):
            return list(transaction.run(query_string))

        with self.driver.session() as session:
            response = list(session.read_transaction(_query_fn))
        return response

    def create_node(self, properties):
        authority, authority_id, enriched_concept = "", "", ""
        if len(properties["ids"]) > 2:
            log.info(len(properties["ids"]))

        for id in properties["ids"]:
            if (
                "lc-names" in id or
                "lc-subjects" in id or
                "nlm-mesh" in id
            ):
                authority, authority_id = id.split("/")
                enriched_concept = enrich(authority, authority_id)
                log.info(enriched_concept)

        self._run_command(
            Pypher().CREATE.node(
                'n', properties["type"],
                id=properties["id"],
                type=properties["type"],
                label=properties["label"],
                authority=authority,
                authority_id=authority_id,
                enrichments=json.dumps(enriched_concept)
            )
        )
        log.info(f"Created {properties['type']}: {properties['label']}")

    def create_edge(self, work_id, concept_id):
        log.info(f"Created edge from {work_id} -> {concept_id}")

    def clear(self, limit=None):
        if limit:
            log.info(f"Clearing {limit} nodes from graph")
            q = Pypher().Match.node("n").WITH("n").LIMIT(limit).DETACH.DELETE("n")
        else:
            log.info("Clearing all nodes from graph")
            q = Pypher().MATCH.node("n").DETACH.DELETE("n")
        self._run_command(q)
        log.info("Cleared graph")

    def get_stats(self):
        q = Pypher()
        q.MATCH.node("n")
        q.RETURN.count(__.n).AS("count")
        return self._run_query(q)

    def get_authority_labelled(self):
        return None
        # (
        #     MATCH(n)
        #     WHERE EXISTS(n.authority_id)
        #     RETURN DISTINCT "node" as entity, n.authority_id AS authority_id
        #     LIMIT 25
        #     UNION ALL
        #     MATCH()-[r]-()
        #     WHERE EXISTS(r.authority_id)
        #     RETURN DISTINCT "relationship" AS entity, r.authority_id AS authority_id
        #     LIMIT 25
        # )
