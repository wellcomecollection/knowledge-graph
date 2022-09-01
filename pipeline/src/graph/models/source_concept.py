from neomodel import (
    ArrayProperty,
    RelationshipFrom,
    StringProperty,
    StructuredNode,
    UniqueIdProperty,
)

from typing import Literal

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
    source_id = StringProperty(unique_index=True, required=True)
    source_type = StringProperty(
        required=True,
        choices={c: c for c in source_types},
    )
    description = StringProperty()
    preferred_label = StringProperty()
    variant_labels = ArrayProperty(StringProperty())
    parent = RelationshipFrom("Concept", "HAS_SOURCE_CONCEPT")
