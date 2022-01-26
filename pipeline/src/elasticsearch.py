from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan

from .prismic import get_fulltext, get_standfirst


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
        contributor.sources.get(source_type="wikidata").preferred_name
        for contributor in story_contributors
    ]
    full_text = get_fulltext(story.wellcome_id)
    standfirst = get_standfirst(story.wellcome_id)
    return {
        "concept_ids": concept_ids,
        "concept_variants": concept_variants,
        "concepts": concept_names,
        "contributors": contributors,
        "contributor_ids": contributor_ids,
        "full_text": full_text,
        "published": story.published,
        "standfirst": standfirst,
        "title": story.title,
        "wikidata_id": story.wikidata_id,
    }


def format_concept_for_elasticsearch(concept):
    concept_stories = concept.stories.all()
    stories = [story.title for story in concept_stories]
    story_ids = [story.wellcome_id for story in concept_stories]
    variants = [
        variant
        for source_concept in concept.sources.all()
        for variant in source_concept.variant_names
    ]

    document = {
        "name": concept.name,
        "stories": stories,
        "story_ids": story_ids,
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


def format_person_for_elasticsearch(person):
    person_stories = (
        person.contributed_to_work.all() + person.contributed_to_story.all()
    )
    stories = [story.title for story in person_stories]
    story_ids = [story.wellcome_id for story in person_stories]
    variants = [
        variant
        for source_concept in person.sources.all()
        for variant in source_concept.variant_names
    ]

    document = {
        "name": person.name,
        "stories": stories,
        "story_ids": story_ids,
        "variants": variants,
    }

    wikidata_source = person.sources.get_or_none(source_type="wikidata")
    if wikidata_source:
        document.update(
            {
                "wikidata_description": wikidata_source.description,
                "wikidata_id": wikidata_source.source_id,
                "wikidata_preferred_name": wikidata_source.preferred_name,
            }
        )

    return document


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
    contributors = [contributor.name for contributor in work_contributors]

    return {
        "concept_ids": concept_ids,
        "concept_variants": concept_variants,
        "concepts": concept_names,
        "contributors": contributors,
        "contributor_ids": contributor_ids,
        "title": work.title,
    }


def yield_all_documents(index_name, host, username, password):
    return scan(
        Elasticsearch(
            host,
            http_auth=(username, password),
            timeout=30,
            retry_on_timeout=True,
            max_retries=10,
        ),
        index=index_name,
        query={
            "query": {
                "bool": {
                    "should": [
                        {"exists": {"field": "data.contributors"}},
                        {"exists": {"field": "data.subjects"}},
                    ],
                    "filter": {"term": {"type": "Visible"}},
                }
            }
        },
        size=10,
        scroll="30m",
        preserve_order=True,
    )
