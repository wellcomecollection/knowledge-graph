from neo4j import GraphDatabase, basic_auth
from pypher import Pypher, __

from weco_datascience.credentials import get_secrets
from weco_datascience.logging import get_logger

log = get_logger(__name__)


class Graph:
    """
    Tidy interface to neo4j aura instance
    """

    def __init__(self):
        log.info("Initialising graph client")
        secrets = get_secrets("neo4j/credentials")

        self.driver = GraphDatabase.driver(
            uri=secrets["connection_uri"],
            auth=basic_auth(
                user=secrets["username"], password=secrets["password"]
            ),
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
                value = '"' + value.replace('"', '\\"') + '"'
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

    def create_node(self, node):
        self._run_command(
            Pypher().MERGE.node(
                "n",
                node["label_type"],
                label=node["label"],
                label_type=node["label_type"],
            )
        )
        log.info(f"Created {node['label_type']}: {node['label']}")

    def create_edge(self, source, target):
        q = Pypher()
        q.MATCH(
            __.node("source", source["label_type"], label=source["label"]),
            __.node("target", target["label_type"], label=target["label"]),
        )
        q.MERGE.node("source").rel_out("r", "rel").node("target")

        self._run_command(q)
        log.info(
            "Created an edge between "
            f"\"{source['label']}\" and \"{target['label']}\""
        )

    def clear(self, limit=None):
        if limit:
            log.info(f"Clearing {limit} nodes from graph")
            q = (
                Pypher()
                .Match.node("n")
                .WITH("n")
                .LIMIT(limit)
                .DETACH.DELETE("n")
            )
        else:
            log.info("Clearing all nodes from graph")
            q = Pypher().MATCH.node("n").DETACH.DELETE("n")
        self._run_command(q)
        log.info("Cleared graph")

    def get_stats(self):
        stats = {
            "nodes": self._run_query(
                Pypher().MATCH.node("n").RETURN.count(__.n).AS("nodes")
            )[0]["nodes"],
            "edges": self._run_query(
                Pypher()
                .MATCH.node("n")
                .rel("r")
                .node()
                .RETURN.count(__.r)
                .AS("edges")
            )[0]["edges"],
            "disconnected": self._run_query(
                Pypher()
                .MATCH.node("n")
                .WHERE.NOT.node("n")
                .rel()
                .node()
                .RETURN.count(__.n)
                .AS("disconnected")
            )[0]["disconnected"],
        }

        return stats

    def search(self, query):
        q = Pypher()
        q.MATCH
        q.node("n", "name", label=query)
        q.rel("*")
        q.node("connected", label_type="name")
        q.RETURN.node("connected")

        variant_names = [
            record["connected"]["label"] for record in self._run_query(q)
        ]
        if variant_names:
            return variant_names + [query]
        else:
            raise ValueError(f'"{query}" isn\'t a node in the graph store ')
