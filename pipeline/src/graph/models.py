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

source_types = [
    "wikidata",
    "wikipedia",
    "lc-subjects",
    "lc-names",
    "nlm-mesh",
    "label-derived",
]
SourceType = Literal[tuple(source_types)]


class SourceConcept(StructuredNode):
    uid = UniqueIdProperty()
    source_id = StringProperty(required=True)
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


class NeighbourRel(StructuredRel):
    source = StringProperty(
        required=True,
        choices={c: c for c in source_types},
    )


class Subject(Concept):
    wellcome_parent_id = StringProperty()
    wellcome_parent_label = StringProperty()
    wellcome_id = StringProperty()
    neighbours = Relationship("Subject", "HAS_NEIGHBOUR", model=NeighbourRel)


class Person(Concept):
    contributions = RelationshipTo("Work", "CONTRIBUTED_TO")



class Work(StructuredNode):
    uid = UniqueIdProperty()
    wellcome_id = StringProperty(required=True)
    wikidata_id = StringProperty()
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
