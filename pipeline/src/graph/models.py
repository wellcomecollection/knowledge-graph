from typing import Literal

from neomodel import (
    ArrayProperty,
    DateProperty,
    Relationship,
    RelationshipFrom,
    RelationshipTo,
    StringProperty,
    StructuredNode,
    StructuredRel,
    UniqueIdProperty,
)

from . import get_logger

log = get_logger(__name__)

source_types = [
    "wikidata",
    "lc-subjects",
    "lc-names",
    "nlm-mesh",
    "label-derived",
]
SourceType = Literal[tuple(source_types)]


class Exhibition(StructuredNode):
    uid = UniqueIdProperty()
    format = StringProperty()
    title = StringProperty(required=True)
    description = StringProperty()
    start_date = DateProperty()
    end_date = DateProperty()
    image_url = StringProperty()
    image_alt = StringProperty()
    location = StringProperty()


class Event(StructuredNode):
    uid = UniqueIdProperty()
    format = StringProperty()
    title = StringProperty(required=True)
    description = StringProperty()
    start_date = DateProperty()
    end_date = DateProperty()
    image_url = StringProperty()
    image_alt = StringProperty()
    location = StringProperty()


class Work(StructuredNode):
    uid = UniqueIdProperty()
    wellcome_id = StringProperty(unique_index=True, required=True)
    wikidata_id = StringProperty(unique_index=True)
    title = StringProperty(required=True)
    # HAS_CONCEPT relationships can be from a Subject or a Person
    concepts = RelationshipFrom("Concept", "HAS_CONCEPT")
    # only Persons can have a CONTRIBUTED_TO relationsip with a work
    contributors = RelationshipFrom("Person", "CONTRIBUTED_TO")
    type = StringProperty(
        required=True,
        choices={c: c for c in ["story", "work"]},
    )
    format = StringProperty()
    published = StringProperty()


class SourceConcept(StructuredNode):
    uid = UniqueIdProperty()
    source_id = StringProperty(unique_index=True, required=True)
    source_type = StringProperty(
        required=True,
        choices={c: c for c in source_types},
    )
    description = StringProperty()
    preferred_label = StringProperty()
    variant_labels = ArrayProperty(StringProperty())
    parent = RelationshipFrom("Concept", "HAS_SOURCE_CONCEPT")


class Concept(StructuredNode):
    label = StringProperty(required=True)
    uid = UniqueIdProperty()
    sources = RelationshipTo("SourceConcept", "HAS_SOURCE_CONCEPT")
    works = RelationshipTo("Work", "HAS_CONCEPT")


class Person(Concept):
    contributions = RelationshipTo("Work", "CONTRIBUTED_TO")


class NeighbourRel(StructuredRel):
    source = StringProperty(
        required=True,
        choices={c: c for c in source_types},
    )


class Subject(Concept):
    wellcome_id = StringProperty(unique_index=True)
    neighbours = Relationship("Subject", "HAS_NEIGHBOUR", model=NeighbourRel)
