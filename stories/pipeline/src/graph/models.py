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

from . import (
    get_lcsh_data,
    get_lcsh_id,
    get_lcsh_preferred_name,
    get_lcsh_variant_names,
    get_mesh_data,
    get_mesh_description,
    get_mesh_id,
    get_mesh_preferred_name,
    get_mesh_variant_names,
    get_wikidata,
    get_wikidata_description,
    get_wikidata_id,
    get_wikidata_preferred_name,
    get_wikidata_variant_names,
)


class BaseConcept(StructuredNode):
    uid = UniqueIdProperty()
    sources = RelationshipTo("SourceConcept", "HAS_SOURCE_CONCEPT")


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
    parent = RelationshipFrom("BaseConcept", "HAS_SOURCE_CONCEPT")


class Concept(BaseConcept):
    name = StringProperty(required=True)
    stories = RelationshipTo("Story", "HAS_CONCEPT")
    neighbours = Relationship("Concept", "IS_NEIGHBOUR_OF")

    def enrich(self, wikidata_id=None):
        if not wikidata_id:
            wikidata_id = get_wikidata_id(concept_name=self.name)

        concept_wikidata = get_wikidata(wikidata_id)
        wikidata_source_concept = SourceConcept(
            source_id=wikidata_id,
            source="wikidata",
            description=get_wikidata_description(concept_wikidata),
            preferred_name=get_wikidata_preferred_name(concept_wikidata),
            variant_names=get_wikidata_variant_names(concept_wikidata),
        ).save()
        self.sources.connect(wikidata_source_concept)

        try:
            lcsh_id = get_lcsh_id(concept_wikidata)
            concept_lcsh_data = get_lcsh_data(lcsh_id)
            lcsh_source_concept = SourceConcept(
                source_id=lcsh_id,
                source="lcsh",
                preferred_name=get_lcsh_preferred_name(concept_lcsh_data),
                variant_names=get_lcsh_variant_names(concept_lcsh_data),
            ).save()
            self.sources.connect(lcsh_source_concept)
        except:
            pass

        try:
            mesh_id = get_mesh_id(concept_wikidata)
            concept_mesh_data = get_mesh_data(mesh_id)
            mesh_source_concept = SourceConcept(
                source_id=mesh_id,
                source="mesh",
                description=get_mesh_description(concept_mesh_data),
                preferred_name=get_mesh_preferred_name(concept_mesh_data),
                variant_names=get_mesh_variant_names(concept_mesh_data),
            ).save()
            self.sources.connect(mesh_source_concept)
        except:
            pass

    def get_neighbours(self):
        for source in self.sources.all():
            if source.source_id == "wikidata":
                self._get_wikidata_neighbours()
            elif source.source_id == "lcsh":
                self._get_lcsh_neighbours()
            elif source.source_id == "mesh":
                self._get_mesh_neighbours()

    def _get_wikidata_neighbours(self):
        wikidata = get_wikidata(self.source_id)
        has_part_ids = [
            part["mainsnak"]["datavalue"]["value"]["id"]
            for part in wikidata["claims"]["P527"]
        ]
        for wikidata_id in has_part_ids:
            concept_wikidata = get_wikidata(wikidata_id)
            neighbour_source_concept = SourceConcept.nodes.get_or_none(
                source_id=wikidata_id
            )
            if neighbour_source_concept:
                neighbour_concept = neighbour_source_concept.parent.all()[0]
            else:
                neighbour_concept = Concept(
                    name=get_wikidata_preferred_name(concept_wikidata)
                ).save()

            self.neighbours.connect(neighbour_concept)
            neighbour_concept.get_enrichments(wikidata_id)

    def _get_lcsh_neighbours(self):
        pass

    def _get_mesh_neighbours(self):
        pass


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
