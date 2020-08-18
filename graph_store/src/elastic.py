from .logging import get_logger
from .credentials import get_secrets
import os

from elasticsearch import Elasticsearch, helpers

log = get_logger(__name__)


class ES:
    def __init__(self):
        log.info("Creating elasticsearch session")
        secrets = get_secrets("reporting/concepts_credentials")
        self.session = Elasticsearch(
            secrets["host"],
            http_auth=(secrets["username"], secrets["password"]),
        )
        log.info("Successfully created elasticsearch session")

    def get_concepts_data(
        self,
        index="concepts_v1",
        query={"query": {"match_all": {}}}
    ):
        log.info(f"fetching data from {index} with query: {str(query)}")
        results_generator = helpers.scan(
            client=self.session,
            index=index,
            query=query,
            request_timeout=14400
        )
        for result in results_generator:
            yield result
