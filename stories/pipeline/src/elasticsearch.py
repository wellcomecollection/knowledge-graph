import os

from elasticsearch import Elasticsearch

from .prismic import get_fulltext, get_standfirst


def get_elasticsearch_session():
    es = Elasticsearch(
        os.environ["ELASTIC_HOST"],
        http_auth=(
            os.environ["ELASTIC_USERNAME"],
            os.environ["ELASTIC_PASSWORD"],
        ),
    )
    return es


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

    contributors = [
        source_concept.preferred_name
        for contributor in story.contributors.all()
        for source_concept in contributor.sources.all()
    ]
    full_text = get_fulltext(story.wellcome_id)
    standfirst = get_standfirst(story.wellcome_id)
    return{
        "concept_ids": concept_ids,
        "concept_variants": concept_variants,
        "concepts": concept_names,
        "contributors": contributors,
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

    wikidata_source = concept.sources.get_or_none(source="wikidata")
    lcsh_source = concept.sources.get_or_none(source="lcsh")
    mesh_source = concept.sources.get_or_none(source="mesh")

    if wikidata_source:
        document.update(
            {
                "wikidata_description": wikidata_source.description,
                "wikidata_id": wikidata_source.source_id,
                "wikidata_preferred_name": wikidata_source.preferred_name,
            }
        )
    if lcsh_source:
        document.update(
            {
                "lcsh_id": lcsh_source.source_id,
                "lcsh_preferred_name": lcsh_source.preferred_name,
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
