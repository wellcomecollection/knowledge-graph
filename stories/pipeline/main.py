import datetime
import json
import os

import pandas as pd

from src.elasticsearch import format_for_indexing, get_elasticsearch_session
from src.enrich import get_variant_names
from src.graph import get_neo4j_session
from src.graph.models import Concept, Contributor, Story, VariantName

print("load stories dataset")
df = pd.read_excel(
    pd.ExcelFile("/data/stories.xlsx", engine="openpyxl"),
    sheet_name="Articles",
    dtype={"Date published": datetime.datetime},
).fillna("")


print("ingest the dataset into neo4j")
db = get_neo4j_session()

print("ingest stories")
stories = {}
for _, story_data in df.iterrows():
    story = Story(
        title=story_data["Title"], published=story_data["Date published"].date()
    ).save()
    stories[story_data["Title"]] = story

print("ingest contributors")
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
    contributor = Contributor(name=name).save()
    contributors[name] = contributor

print("ingest concepts")
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
    concept = Concept(name=name).save()
    concepts[name] = concept

for _, story_data in df.iterrows():
    story = stories[story_data["Title"]]

    contributor_names = [
        name.strip()
        for name in (
            story_data["Author"].split(
                ",") + story_data["Images by"].split(",")
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


print("enrich concepts with variant names")
variants = {concept: get_variant_names(concept) for concept in unique_concepts}

all_variant_name_edges = [
    (concept_core_name, variant_name)
    for concept_core_name, variant_names in variants.items()
    for variant_name in variant_names
    if variant_name != concept_core_name
]

unique_variant_names = list(set([edge[1] for edge in all_variant_name_edges]))

variant_dict = {}
for variant_name in unique_variant_names:
    v = VariantName(name=variant_name).save()
    variant_dict[variant_name] = v

for concept_core_name, variant_name in all_variant_name_edges:
    concept = concepts[concept_core_name]
    variant = variant_dict[variant_name]
    concept.variant_names.connect(variant)


print("unpack the graph into elasticsearch")
es = get_elasticsearch_session()
stories_index_name = os.environ["STORIES_INDEX_NAME"]
concepts_index_name = os.environ["CONCEPTS_INDEX_NAME"]

print("create the stories index")
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
print("populate the stories index")
for story in Story.nodes.all():
    concepts_on_node = [concept.name for concept in story.concepts.all()]
    variants_on_concepts_on_node = [
        variant.name
        for concept in story.concept.all()
        for variant in concept.variant_name.all()
    ]

    es.index(
        index=stories_index_name,
        document=format_for_indexing(
            {
                "title": story.title,
                "published": story.published,
                "concepts": concepts_on_node,
                "variants": variants_on_concepts_on_node,
            }
        ),
    )

print("create the concepts index")
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

print("populate the concepts index")
for concept in Concept.nodes.all():
    stories = [story.name for story in concept.stories.all()]
    variants = [variant.name for variant in concept.variant_name.all()]

    es.index(
        index=concepts_index_name,
        document=format_for_indexing(
            {"name": story.title, "stories": stories, "variants": variants}
        ),
    )
