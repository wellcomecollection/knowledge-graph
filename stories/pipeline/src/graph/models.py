from neomodel import (
    ArrayProperty,
    DateProperty,
    Relationship,
    RelationshipFrom,
    RelationshipTo,
    StringProperty,
    StructuredNode,
    UniqueIdProperty,
)


class BaseConcept(StructuredNode):
    __abstract_node__ = True
    uid = UniqueIdProperty()
    sources = RelationshipFrom("SourceConcept", "HAS_SOURCE_CONCEPT")


class Concept(BaseConcept):
    name = StringProperty()
    stories = RelationshipTo("Story", "HAS_CONCEPT")
    neighbours = Relationship("Concept", "IS_NEIGHBOUR_OF")


class SourceConcept(StructuredNode):
    uid = UniqueIdProperty()
    source_id = StringProperty(unique_index=True, required=True)
    source = StringProperty(
        required=True,
        choices={"wikidata": "wikidata", "lcsh": "lcsh", "mesh": "mesh"},
    )
    description = StringProperty()
    preferred_name = StringProperty()
    variant_names = ArrayProperty(StringProperty())
    parent = RelationshipTo("Concept", "HAS_SOURCE_CONCEPT")


class Person(BaseConcept):
    contributed_to = RelationshipTo("Story", "CONTRIBUTED_TO")
    is_about = RelationshipFrom("Story", "IS_ABOUT")


class Story(StructuredNode):
    uid = UniqueIdProperty()
    wellcome_id = StringProperty(unique_index=True, required=True)
    published = DateProperty(required=True)
    title = StringProperty(required=True)
    wikidata_id = StringProperty(unique_index=True)
    concepts = RelationshipFrom("Concept", "HAS_CONCEPT")
    contributors = RelationshipFrom("Person", "CONTRIBUTED_TO")
    subjects = RelationshipTo("Person", "IS_ABOUT")
