from neomodel import (
    Relationship,
    RelationshipTo,
    StringProperty,
    StructuredNode,
    StructuredRel,
    UniqueIdProperty,
)

from .source_concept import source_types


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
    wellcome_id = StringProperty(unique_index=True)
    neighbours = Relationship("Subject", "HAS_NEIGHBOUR", model=NeighbourRel)


class Person(Concept):
    contributions = RelationshipTo("Work", "CONTRIBUTED_TO")
