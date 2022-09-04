import os
from pydoc import doc

from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan

from ..graph.models import Concept, Event, Exhibition, Work
from ..prismic import (
    get_story_data,
    get_story_fulltext,
    get_story_image,
    get_story_standfirst,
)
from ..utils import get_logger
from ..wellcome import (
    get_work_data,
    get_work_dates,
    get_work_description,
    get_work_image,
    get_work_notes,
)

ordered_source_preferences = ["wikidata", "nlm-mesh", "lc-subjects", "lc-names"]

log = get_logger(__name__)


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


def yield_works(size=10_000):
    pipeline_es_client = get_pipeline_es_client()
    works_generator = scan(
        pipeline_es_client,
        index=os.environ["ELASTIC_PIPELINE_WORKS_INDEX"],
        query={
            "query": {
                "bool": {
                    "filter": [
                        {"term": {"type": "Visible"}},
                    ],
                }
            },
            "size": size,
        },
        size=10,
        scroll="30m",
        preserve_order=True,
    )
    for document in works_generator:
        try:
            work = document["_source"]["data"]
            work["_id"] = document["_id"]
            yield work
        except KeyError as error:
            log.error("No data found in document", error=error)
            continue


def yield_popular_works(size=10_000):
    reporting_es_client = get_reporting_es_client()
    response = reporting_es_client.search(
        index="metrics-conversion-prod",
        size=0,
        query={
            "query": {
                "bool": {
                    "must": [
                        {"term": {"page.name": {"value": "work"}}},
                        {"range": {"@timestamp": {"gte": "2021-09-01"}}},
                    ]
                }
            },
            "aggs": {
                "popular_works": {
                    "terms": {"field": "page.query.id", "size": size}
                }
            },
        },
    )
    popular_work_ids = [
        bucket["key"]
        for bucket in response["aggregations"]["popular_works"]["buckets"]
    ]

    pipeline_es_client = get_pipeline_es_client()
    works_generator = scan(
        pipeline_es_client,
        index=os.environ["ELASTIC_PIPELINE_WORKS_INDEX"],
        query={
            "query": {
                "bool": {
                    "should": [
                        {"exists": {"field": "data.contributors"}},
                        {"exists": {"field": "data.subjects"}},
                    ],
                    "filter": [
                        {"term": {"type": "Visible"}},
                        {"terms": {"_id": popular_work_ids}},
                    ],
                }
            }
        },
        size=10,
        scroll="30m",
        preserve_order=True,
    )
    for document in works_generator:
        try:
            work = document["_source"]["data"]
            work["_id"] = document["_id"]
            yield work
        except KeyError as e:
            log.error("No data found in document", error=e)
            continue
