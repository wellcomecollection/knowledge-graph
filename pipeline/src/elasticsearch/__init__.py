import os

from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan

from ..graph.models import Concept
from ..prismic import get_fulltext, get_slices, get_standfirst
from ..utils import get_logger
from ..wellcome import get_description, get_notes, get_work_data

ordered_source_preferences = ["wikidata", "nlm-mesh", "lc-subjects", "lc-names"]


def get_concepts_es_client():
    concepts_es_client = Elasticsearch(
        os.environ["ELASTIC_CONCEPTS_HOST"],
        http_auth=(
            os.environ["ELASTIC_CONCEPTS_USERNAME"],
            os.environ["ELASTIC_CONCEPTS_PASSWORD"],
        ),
    )
    return concepts_es_client


def get_reporting_es_client():
    reporting_es_client = Elasticsearch(
        os.environ["ELASTIC_REPORTING_HOST"],
        http_auth=(
            os.environ["ELASTIC_REPORTING_USERNAME"],
            os.environ["ELASTIC_REPORTING_PASSWORD"],
        ),
        timeout=30,
        retry_on_timeout=True,
        max_retries=10,
    )
    return reporting_es_client


def get_pipeline_es_client():
    pipeline_es_client = Elasticsearch(
        os.environ["ELASTIC_PIPELINE_HOST"],
        http_auth=(
            os.environ["ELASTIC_PIPELINE_USERNAME"],
            os.environ["ELASTIC_PIPELINE_PASSWORD"],
        ),
        timeout=30,
        retry_on_timeout=True,
        max_retries=10,
    )
    return pipeline_es_client
