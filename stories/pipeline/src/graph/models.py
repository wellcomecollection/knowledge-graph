from neomodel import (
    DateProperty,
    RelationshipFrom,
    RelationshipTo,
    StringProperty,
    StructuredNode,
    UniqueIdProperty,
)


class Concept(StructuredNode):
    uid = UniqueIdProperty()
    name = StringProperty(unique_index=True, required=True)
    variant_names = RelationshipTo("VariantName", "AKA")
    stories = RelationshipTo("Story", "HAS_CONCEPT")


class Contributor(StructuredNode):
    uid = UniqueIdProperty()
    name = StringProperty(unique_index=True, required=True)
    variant_names = RelationshipTo("VariantName", "AKA")
    stories = RelationshipTo("Story", "CONTRIBUTED_TO")


class Story(StructuredNode):
    uid = UniqueIdProperty()
    title = StringProperty(unique_index=True, required=True)
    published = DateProperty()
    contributors = RelationshipFrom("Contributor", "CONTRIBUTED_TO")
    concepts = RelationshipFrom("Concept", "HAS_CONCEPT")


class VariantName(StructuredNode):
    uid = UniqueIdProperty()
    name = StringProperty(unique_index=True, required=True)
    concepts = RelationshipFrom("Concept", "AKA")
