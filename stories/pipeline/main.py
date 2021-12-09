import datetime
import json
import os
from pathlib import Path

import pandas as pd
from structlog import get_logger

from src.elasticsearch import get_elasticsearch_session
from src.enrich.lcsh import (
    get_lcsh_data,
    get_lcsh_id,
    get_lcsh_preferred_name,
    get_lcsh_variant_names,
)
from src.enrich.mesh import (
    get_mesh_data,
    get_mesh_description,
    get_mesh_id,
    get_mesh_preferred_name,
    get_mesh_variant_names,
)
from src.enrich.wikidata import (
    get_contributor_wikidata_ids,
    get_wikidata,
    get_wikidata_description,
    get_wikidata_id,
    get_wikidata_preferred_name,
    get_wikidata_variant_names,
)
from src.graph import get_neo4j_session
from src.graph.models import Concept, Person, SourceConcept, Story
from src.prismic import get_fulltext, get_standfirst
from src.utils import clean_csv

log = get_logger()


log.info("Loading stories dataset")
df = (
    pd.read_excel(
        pd.ExcelFile("/data/stories.xlsx", engine="openpyxl"),
        sheet_name="Articles",
        dtype={"Date published": datetime.datetime},
    )
    .fillna("")
)


log.info("Connecting to neo4j")
db = get_neo4j_session()


log.info("Processing stories")
stories = {}
people = {}
concepts = {}
for _, story_data in df.iterrows():
    log.info("Creating story", story=story_data["Title"])
    story = Story(
        wellcome_id=Path(story_data["URL"]).name,
        title=story_data["Title"],
        published=story_data["Date published"].date(),
        wikidata_id=story_data["Wikidata ID"],
    ).save()
    stories[story.wellcome_id] = story

    log.debug("Fetching wikidata for story", story=story.title)
    story_wikidata = get_wikidata(story.wikidata_id)

    contributor_wikidata_ids = get_contributor_wikidata_ids(story_wikidata)
    for contributor_wikidata_id in contributor_wikidata_ids:
        if contributor_wikidata_id in people:
            person = people[contributor_wikidata_id]
        else:
            log.debug(
                "Fetching wikidata for person",
                contributor_wikidata_id=contributor_wikidata_id,
            )
            contributor_wikidata = get_wikidata(contributor_wikidata_id)
            source_concept = SourceConcept(
                source_id=contributor_wikidata_id,
                source="wikidata",
                description=get_wikidata_description(contributor_wikidata),
                preferred_name=get_wikidata_preferred_name(
                    contributor_wikidata
                ),
                variant_names=get_wikidata_variant_names(contributor_wikidata),
            ).save()
            log.info(
                "Creating person",
                contributor_wikidata_id=contributor_wikidata_id,
            )
            person = Person().save()
            person.sources.connect(source_concept)
            people[contributor_wikidata_id] = person
        log.debug(
            "Connecting contributor to story",
            person=person.sources.all()[0].preferred_name,
            story=story.title,
        )
        story.contributors.connect(person)

    for concept_name in clean_csv(story_data["Keywords"]):
        if concept_name in concepts:
            concept = concepts[concept_name]
        else:
            log.info(
                "Creating concept", concept_name=concept_name,
            )
            concept = Concept(name=concept_name).save()
            try:
                log.debug(
                    "Fetching wikidata for concept", concept_name=concept_name
                )
                concept_wikidata_id = get_wikidata_id(concept_name)
                concept_wikidata = get_wikidata(concept_wikidata_id)
                wikidata_source_concept = SourceConcept(
                    source_id=concept_wikidata_id,
                    source="wikidata",
                    description=get_wikidata_description(concept_wikidata),
                    preferred_name=get_wikidata_preferred_name(
                        concept_wikidata
                    ),
                    variant_names=get_wikidata_variant_names(concept_wikidata),
                ).save()
                log.debug(
                    "Connecting concept to wikidata source concept",
                    concept_name=concept_name,
                    wikidata_id=concept_wikidata_id,
                )
                concept.sources.connect(wikidata_source_concept)

                try:
                    lcsh_id = get_lcsh_id(concept_wikidata)
                    log.debug(
                        "Fetching lcsh data for concept",
                        concept_name=concept_name,
                    )
                    concept_lcsh_data = get_lcsh_data(lcsh_id)
                    lcsh_source_concept = SourceConcept(
                        source_id=lcsh_id,
                        source="lcsh",
                        preferred_name=get_lcsh_preferred_name(
                            concept_lcsh_data
                        ),
                        variant_names=get_lcsh_variant_names(concept_lcsh_data),
                    ).save()
                    log.debug(
                        "Connecting concept to lcsh source concept",
                        concept_name=concept_name,
                        lcsh_id=lcsh_id,
                    )
                    concept.sources.connect(lcsh_source_concept)
                except:
                    pass

                try:
                    mesh_id = get_mesh_id(concept_wikidata)
                    log.debug(
                        "Fetching mesh data for concept",
                        concept_name=concept_name,
                    )
                    concept_mesh_data = get_mesh_data(mesh_id)
                    mesh_source_concept = SourceConcept(
                        source_id=mesh_id,
                        source="mesh",
                        description=get_mesh_description(concept_mesh_data),
                        preferred_name=get_mesh_preferred_name(
                            concept_mesh_data
                        ),
                        variant_names=get_mesh_variant_names(concept_mesh_data),
                    ).save()
                    log.debug(
                        "Connecting concept to mesh source concept",
                        concept_name=concept_name,
                        mesh_id=mesh_id,
                    )
                    concept.sources.connect(mesh_source_concept)
                except:
                    pass

            except:
                pass
            concepts[concept_name] = concept
        log.debug(
            "Connecting concept to story",
            concept_name=concept_name,
            story=story.title,
        )
        story.concepts.connect(concept)

log.info("Unpacking the graph into elasticsearch")
es = get_elasticsearch_session()
stories_index_name = os.environ["ELASTIC_STORIES_INDEX"]

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

    es.index(
        index=stories_index_name,
        id=story.wellcome_id,
        document={
            "concept_ids": concept_ids,
            "concept_variants": concept_variants,
            "concepts": concept_names,
            "contributors": contributors,
            "full_text": full_text,
            "published": story.published,
            "standfirst": standfirst,
            "title": story.title,
            "wikidata_id": story.wikidata_id,
        },
    )

concepts_index_name = os.environ["ELASTIC_CONCEPTS_INDEX"]
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
    variants = [
        variant
        for source_concept in concept.sources.all()
        for variant in source_concept.variant_names
    ]

    wikidata_source = concept.sources.get_or_none(source="wikidata")
    lcsh_source = concept.sources.get_or_none(source="lcsh")
    mesh_source = concept.sources.get_or_none(source="mesh")

    es.index(
        index=concepts_index_name,
        id=concept.uid,
        document={
            "lcsh_id": lcsh_source.source_id if lcsh_source else None,
            "lcsh_preferred_name": lcsh_source.preferred_name
            if lcsh_source
            else None,
            "mesh_description": mesh_source.description
            if mesh_source
            else None,
            "mesh_id": mesh_source.source_id if mesh_source else None,
            "mesh_preferred_name": mesh_source.preferred_name
            if mesh_source
            else None,
            "name": concept.name,
            "stories": stories,
            "story_ids": story_ids,
            "variants": variants,
            "wikidata_description": wikidata_source.description
            if wikidata_source
            else None,
            "wikidata_id": wikidata_source.source_id
            if wikidata_source
            else None,
            "wikidata_preferred_name": wikidata_source.preferred_name
            if wikidata_source
            else None,
        },
    )
