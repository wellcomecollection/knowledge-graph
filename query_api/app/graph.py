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
            unique_variants = set(variant_names + [query])
            return unique_variants
        else:
            raise ValueError(f"'{query}' isn't a node in the graph store")
