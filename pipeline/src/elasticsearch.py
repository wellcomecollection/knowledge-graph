import os

from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan

from .prismic import get_fulltext, get_slices, get_standfirst
from .wellcome import get_description, get_notes, get_work_data


def format_work_for_elasticsearch(work):
    work_concepts = work.concepts.all()
    concept_ids = [concept.uid for concept in work_concepts]
    concept_names = [concept.name for concept in work_concepts]
    concept_variants = [
        variant
        for concept in work_concepts
        for source_concept in concept.sources.all()
        for variant in source_concept.variant_names
    ]

    work_contributors = work.contributors.all()
    contributor_ids = [contributor.uid for contributor in work_contributors]
    contributors = [
        source_concept.preferred_name
        for contributor in work_contributors
        for source_concept in contributor.sources.all()
    ]

    work_data = get_work_data(work.wellcome_id)
    description = get_description(work_data)
    notes = get_notes(work_data)

    return {
        "concept_ids": concept_ids,
        "concept_variants": concept_variants,
        "concepts": concept_names,
        "contributors": contributors,
        "contributor_ids": contributor_ids,
        "contributors": contributors,
        "published": work.published,
        "title": work.title,
        "description": description,
        "notes": notes,
    }


def format_story_for_elasticsearch(story):
    story_concepts = story.concepts.all()
    concept_ids = [concept.uid for concept in story_concepts]
    concept_names = [concept.name for concept in story_concepts]
    concept_variants = [
        variant
        for concept in story_concepts
        for source_concept in concept.sources.all()
        for variant in source_concept.variant_names
    ]

    story_contributors = story.contributors.all()
    contributor_ids = [contributor.uid for contributor in story_contributors]
    contributors = [
        source_concept.preferred_name
        for contributor in story_contributors
        for source_concept in contributor.sources.all()
    ]
    slices = get_slices(story.wellcome_id)
    full_text = get_fulltext(slices)
    standfirst = get_standfirst(slices)

    return {
        "concept_ids": concept_ids,
        "concept_variants": concept_variants,
        "concepts": concept_names,
        "contributor_ids": contributor_ids,
        "contributors": contributors,
        "contributors": contributors,
        "full_text": full_text,
        "published": story.published,
        "standfirst": standfirst,
        "title": story.title,
    }


def format_concept_for_elasticsearch(concept):
    concept_works = concept.works.all()
    works = [story.title for story in concept_works]
    work_ids = [story.wellcome_id for story in concept_works]
    variants = [
        variant
        for source_concept in concept.sources.all()
        for variant in source_concept.variant_names
    ]

    document = {
        "name": concept.name,
        "type": concept.type,
        "works": works,
        "work_ids": work_ids,
        "variants": variants,
    }

    wikidata_source = concept.sources.get_or_none(source_type="wikidata")
    lc_subjects_source = concept.sources.get_or_none(source_type="lc-subjects")
    lc_names_source = concept.sources.get_or_none(source_type="lc-names")
    mesh_source = concept.sources.get_or_none(source_type="nlm-mesh")

    if wikidata_source:
        document.update(
            {
                "wikidata_description": wikidata_source.description,
                "wikidata_id": wikidata_source.source_id,
                "wikidata_preferred_name": wikidata_source.preferred_name,
            }
        )
    if lc_subjects_source:
        document.update(
            {
                "lc_subjects_id": lc_subjects_source.source_id,
                "lcsh_preferred_name": lc_subjects_source.preferred_name,
            }
        )
    if lc_names_source:
        document.update(
            {
                "lc_names_id": lc_names_source.source_id,
                "lcsh_preferred_name": lc_names_source.preferred_name,
            }
        )
    if mesh_source:
        document.update(
            {
                "mesh_description": mesh_source.description,
                "mesh_id": mesh_source.source_id,
                "mesh_preferred_name": mesh_source.preferred_name,
            }
        )

    return document


def yield_popular_works(size=10_000):
    reporting_es = Elasticsearch(
        os.environ["ELASTIC_REPORTING_HOST"],
        http_auth=(
            os.environ["ELASTIC_REPORTING_USERNAME"],
            os.environ["ELASTIC_REPORTING_PASSWORD"],
        ),
        timeout=30,
        retry_on_timeout=True,
        max_retries=10,
    )

    response = reporting_es.search(
        index="metrics-conversion-prod",
        body={
            "size": 0,
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

    pipeline_es = Elasticsearch(
        os.environ["ELASTIC_PIPELINE_HOST"],
        http_auth=(
            os.environ["ELASTIC_PIPELINE_USERNAME"],
            os.environ["ELASTIC_PIPELINE_PASSWORD"],
        ),
        timeout=30,
        retry_on_timeout=True,
        max_retries=10,
    )
    works_generator = scan(
        pipeline_es,
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
    return works_generator
