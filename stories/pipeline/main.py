import datetime
import json
import os
from pathlib import Path

import pandas as pd
from structlog import get_logger

from src.elasticsearch import (
    format_concept_for_elasticsearch,
    format_story_for_elasticsearch,
    get_elasticsearch_session,
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
    .head(20)
)


log.info("Connecting to neo4j")
db = get_neo4j_session()


log.info("Processing stories")
for _, story_data in df.iterrows():
    story_id = Path(story_data["URL"]).name
    log.info("Processing story", story_id=story_id)
    story = Story(
        wellcome_id=story_id,
        title=story_data["Title"],
        published=story_data["Date published"].date(),
        wikidata_id=story_data["Wikidata ID"],
    ).save()

    story_wikidata = get_wikidata(story.wikidata_id)
    contributor_wikidata_ids = get_contributor_wikidata_ids(story_wikidata)
    for contributor_wikidata_id in contributor_wikidata_ids:
        existing_person_source_concept = SourceConcept.nodes.get_or_none(
            source_id=contributor_wikidata_id
        )
        if existing_person_source_concept:
            person = existing_person_source_concept.parent.all()[0]
        else:
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
            person = Person().save()
            person.sources.connect(source_concept)
        story.contributors.connect(person)

    for concept_name in clean_csv(story_data["Keywords"]):
        concept_wikidata_id = get_wikidata_id(concept_name)
        if concept_wikidata_id:
            existing_concept_source_concept = SourceConcept.nodes.get_or_none(
                source_id=concept_wikidata_id
            )
            if existing_concept_source_concept:
                concept = existing_concept_source_concept.parent.all()[0]
            else:
                concept = Concept(name=concept_name).save()
                concept.enrich(wikidata_id=concept_wikidata_id)
        else:
            concept = Concept(name=concept_name).save()
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
    es.index(
        index=stories_index_name,
        id=story.wellcome_id,
        document=format_story_for_elasticsearch(story),
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
    es.index(
        index=concepts_index_name,
        id=concept.uid,
        document=format_concept_for_elasticsearch(concept),
    )
