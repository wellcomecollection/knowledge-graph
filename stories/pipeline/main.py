import datetime
import json
import os
from pathlib import Path

import pandas as pd
from structlog import get_logger

from src.elasticsearch import format_for_indexing, get_elasticsearch_session
from src.enrich import get_variant_names
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


log.info("Ingesting the dataset into neo4j")
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


log.info("Ingesting concepts")
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

concepts = {}
for name in unique_concepts:
    log.debug("Ingesting concept", name=name)
    concept = Concept(name=name).save()
    concepts[name] = concept

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
        concept = concepts[name]
        story.concepts.connect(concept)


log.info("Enriching the concepts with variant names")
variants = {}
for concept in unique_concepts:
    log.debug("Enriching concept", concept=concept)
    variants[concept] = get_variant_names(concept)

all_variant_name_edges = [
    (concept_core_name, variant_name)
    for concept_core_name, variant_names in variants.items()
    for variant_name in variant_names
    if variant_name != concept_core_name
]

unique_variant_names = list(set([edge[1] for edge in all_variant_name_edges]))

variant_dict = {}
for variant_name in unique_variant_names:
    log.debug("Ingesting variant name", variant_name=variant_name)
    v = VariantName(name=variant_name).save()
    variant_dict[variant_name] = v

for concept_core_name, variant_name in all_variant_name_edges:
    log.debug(
        "Creating edge for variant name",
        concept_core_name=concept_core_name,
        variant_name=variant_name,
    )
    concept = concepts[concept_core_name]
    variant = variant_dict[variant_name]
    concept.variant_names.connect(variant)


log.info("Unpacking the graph into elasticsearch")
es = get_elasticsearch_session()
stories_index_name = os.environ["ELASTIC_STORIES_INDEX_NAME"]
concepts_index_name = os.environ["ELASTIC_CONCEPTS_INDEX_NAME"]

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
    concepts_on_node = list(
        set([concept.name for concept in story.concepts.all()])
    )
    variants_on_concepts_on_node = list(
        set(
            [
                variant.name
                for concept in story.concepts.all()
                for variant in concept.variant_names.all()
            ]
        )
    )

    contributors = [
        contributor.name for contributor in story.contributors.all()
    ]
    full_text = get_fulltext(story.wellcome_id)
    standfirst = get_standfirst(story.wellcome_id)

    es.index(
        index=stories_index_name,
        document=format_for_indexing(
            {
                "concepts": concepts_on_node,
                "concepts_variants": variants_on_concepts_on_node,
                "contributors": contributors,
                "full_text": full_text,
                "wellcome_id": story.wellcome_id,
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
    stories = [story.title for story in concept.stories.all()]
    variants = [variant.name for variant in concept.variant_names.all()]

    es.index(
        index=concepts_index_name,
        document=format_for_indexing(
            {
                "id": concept.uid,
                "name": concept.name,
                "stories": stories,
                "variants": variants,
            }
        ),
    )
