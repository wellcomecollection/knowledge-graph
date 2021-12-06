import os

from elasticsearch import Elasticsearch


def get_elasticsearch_session():
    es = Elasticsearch(
        os.environ["ELASTIC_HOST"],
        http_auth=(
            os.environ["ELASTIC_USERNAME"],
            os.environ["ELASTIC_PASSWORD"],
        ),
    )
    return es

