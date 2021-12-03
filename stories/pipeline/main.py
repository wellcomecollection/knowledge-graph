import datetime
import json
import os
from pathlib import Path

import pandas as pd
from structlog import get_logger

from src.elasticsearch import format_for_indexing, get_elasticsearch_session
from src.enrich import enrich
from src.graph import get_neo4j_session
from src.graph.models import Concept, Contributor, Story, VariantName
from src.prismic import get_fulltext, get_standfirst

log = get_logger()


log.info("Loading stories dataset")
df = pd.read_excel(
    pd.ExcelFile("/data/stories.xlsx", engine="openpyxl"),
    sheet_name="Articles",
    dtype={"Date published": datetime.datetime},
).fillna("")


log.info("Connecting to neo4j")
db = get_neo4j_session()


log.info("Ingesting stories")
stories = {}
for _, story_data in df.iterrows():
    log.debug("Ingesting story", title=story_data["Title"])
    story = Story(
        wellcome_id=Path(story_data["URL"]).name,
        title=story_data["Title"],
        published=story_data["Date published"].date(),
        wikidata_id=story_data["Wikidata ID"],
    ).save()
    stories[story.wellcome_id] = story


log.info("Ingesting contributors")
unique_contributors = list(
    set(
        [
            name.strip()
            for authors, images_by in df[["Author", "Images by"]].values
            for name in (authors.split(",") + images_by.split(","))
            if name.strip() != ""
        ]
    )
)

contributors = {}
for name in unique_contributors:
    log.debug("Ingesting contributor", name=name)
    contributor = Contributor(name=name).save()
    contributors[name] = contributor


log.info("Enriching concepts")
unique_concepts = list(
    set(
        [
            concept.strip()
            for concepts in df["Keywords"].values
            for concept in concepts.split(",")
            if concept.strip() != ""
        ]
    )
)

enriched_concepts = {}
for concept_name in unique_concepts:
    log.debug("Enriching concept", concept_name=concept_name)
    enriched_concepts[concept_name] = enrich(concept_name)


log.info("Ingesting concepts")
concepts_dict = {}
for concept_name in unique_concepts:
    log.debug("Ingesting concept", concept_name=concept_name)
    enriched_concept = enriched_concepts[concept_name]
    concept = Concept(
        name=concept_name,
        wikidata_preferred_name=enriched_concept["wikidata"]["preferred_name"],
        mesh_preferred_name=enriched_concept["mesh"]["preferred_name"],
        lcsh_preferred_name=enriched_concept["lcsh"]["preferred_name"],
        wikidata_description=enriched_concept["wikidata"]["description"],
        mesh_description=enriched_concept["mesh"]["description"],
    ).save()
    concepts_dict[concept_name] = concept


log.info(
    "Creating edges between stories, contributors, concepts and variant names"
)
for _, story_data in df.iterrows():
    log.debug("Creating edges for story", title=story_data["Title"])
    story = stories[Path(story_data["URL"]).name]

    contributor_names = [
        name.strip()
        for name in (
            story_data["Author"].split(",") + story_data["Images by"].split(",")
        )
        if name.strip() != ""
    ]
    for name in contributor_names:
        contributor = contributors[name]
        story.contributors.connect(contributor)

    concept_names = [
        concept.strip()
        for concept in story_data["Keywords"].split(",")
        if concept.strip() != ""
    ]
    for name in concept_names:
        concept = concepts_dict[name]
        story.concepts.connect(concept)


unique_variants = list(
    set(
        [
            (variant, source)
            for _, all_enrichments in enriched_concepts.items()
            for source, source_enrichments in all_enrichments.items()
            for variant in source_enrichments["variants"]
        ]
    )
)

log.info("Ingesting variant name", name=name)
variant_dict = {}
for name, source in unique_variants:
    log.debug("Ingesting variant name", name=name)
    v = VariantName(name=name, source=source).save()
    variant_dict[hash((name, source))] = v

for concept_name, all_enrichments in enriched_concepts.items():
    for source, source_enrichments in all_enrichments.items():
        for variant_name in source_enrichments["variants"]:
            log.debug(
                "Creating edge",
                concept_name=concept_name,
                variant_name=variant_name,
            )
            concept = concepts_dict[concept_name]
            variant = variant_dict[hash((variant_name, source))]
            concept.variant_names.connect(variant)


log.info("Unpacking the graph into elasticsearch")
es = get_elasticsearch_session()
stories_index_name = os.environ["ELASTIC_STORIES_INDEX"]
concepts_index_name = os.environ["ELASTIC_CONCEPTS_INDEX"]

log.info(f"Create the stories index: {stories_index_name}")
with open("/data/elastic/stories/mapping.json", "r") as f:
    stories_mappings = json.load(f)
with open("/data/elastic/stories/settings.json", "r") as f:
    stories_settings = json.load(f)

es.indices.delete(index=stories_index_name, ignore=404)
es.indices.create(
    index=stories_index_name,
    mappings=stories_mappings,
    settings=stories_settings,
)


log.info("Populating the stories index")
for story in Story.nodes.all():
    log.debug("Indexing story", story=story.title)

    story_concepts = story.concepts.all()
    concept_names = [concept.name for concept in story_concepts]
    concept_ids = [concept.uid for concept in story_concepts]
    concept_variants = [
        variant.name
        for concept in story_concepts
        for variant in concept.variant_names.all()
    ]

    contributors = [
        contributor.name for contributor in story.contributors.all()
    ]

    full_text = get_fulltext(story.wellcome_id)
    standfirst = get_standfirst(story.wellcome_id)

    es.index(
        index=stories_index_name,
        id=story.wellcome_id,
        document=format_for_indexing(
            {
                "concepts": concept_names,
                "concept_ids": concept_ids,
                "concept_variants": concept_variants,
                "contributors": contributors,
                "full_text": full_text,
                "published": story.published,
                "standfirst": standfirst,
                "title": story.title,
                "wikidata_id": story.wikidata_id,
            }
        ),
    )


log.info(f"Creating the concepts index: {concepts_index_name}")
with open("/data/elastic/concepts/mapping.json", "r") as f:
    concepts_mappings = json.load(f)
with open("/data/elastic/concepts/settings.json", "r") as f:
    concepts_settings = json.load(f)

es.indices.delete(index=concepts_index_name, ignore=404)
es.indices.create(
    index=concepts_index_name,
    mappings=concepts_mappings,
    settings=concepts_settings,
)


log.info("Populating the concepts index")
for concept in Concept.nodes.all():
    log.debug("Indexing concept", concept=concept.name)
    concept_stories = concept.stories.all()
    stories = [story.title for story in concept_stories]
    story_ids = [story.wellcome_id for story in concept_stories]
    variants = [variant.name for variant in concept.variant_names.all()]

    es.index(
        index=concepts_index_name,
        id=concept.uid,
        document=format_for_indexing(
            {
                "name": concept.name,
                "wikidata_id": concept.wikidata_id,
                "mesh_id": concept.mesh_id,
                "lcsh_id": concept.lcsh_id,
                "wikidata_preferred_name": concept.wikidata_preferred_name,
                "mesh_preferred_name": concept.mesh_preferred_name,
                "lcsh_preferred_name": concept.lcsh_preferred_name,
                "wikidata_description": concept.wikidata_description,
                "mesh_description": concept.mesh_description,
                "stories": stories,
                "story_ids": story_ids,
                "variants": variants,
            }
        ),
    )
