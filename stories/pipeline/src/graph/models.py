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
    wikidata_preferred_name = StringProperty()
    mesh_preferred_name = StringProperty()
    lcsh_preferred_name = StringProperty()
    wikidata_id = StringProperty()
    mesh_id = StringProperty()
    lcsh_id = StringProperty()
    wikidata_description = StringProperty()
    mesh_description = StringProperty()
    stories = RelationshipTo("Story", "HAS_CONCEPT")
    variant_names = RelationshipTo("VariantName", "AKA")


class Contributor(StructuredNode):
    uid = UniqueIdProperty()
    name = StringProperty(required=True)
    stories = RelationshipTo("Story", "CONTRIBUTED_TO")
    variant_names = RelationshipTo("VariantName", "AKA")


class Story(StructuredNode):
    uid = UniqueIdProperty()
    concepts = RelationshipFrom("Concept", "HAS_CONCEPT")
    contributors = RelationshipFrom("Contributor", "CONTRIBUTED_TO")
    published = DateProperty(required=True)
    title = StringProperty(required=True)
    wellcome_id = StringProperty(unique_index=True, required=True)
    wikidata_id = StringProperty(unique_index=True)


class VariantName(StructuredNode):
    uid = UniqueIdProperty()
    concepts = RelationshipFrom("Concept", "AKA")
    name = StringProperty(required=True)
    source = StringProperty(required=True)
