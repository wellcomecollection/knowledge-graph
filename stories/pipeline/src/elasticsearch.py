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


def format_for_indexing(document):
    for key, value in document.items():
        if isinstance(value, list):
            document[key] = "<BREAK>".join([str(x) for x in value])
    return document
