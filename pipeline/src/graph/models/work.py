from neomodel import (
    RelationshipFrom,
    StringProperty,
    StructuredNode,
    UniqueIdProperty,
)


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
