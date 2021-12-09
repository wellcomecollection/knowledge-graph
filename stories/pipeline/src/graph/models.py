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

from structlog import get_logger

log = get_logger()


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
        log.debug("Enriching concept", wikidata_id=wikidata_id)
        wikidata_source_concept = SourceConcept.nodes.get_or_none(
            source_id=wikidata_id, source="wikidata"
        )
        if not wikidata_source_concept:
            concept_wikidata = get_wikidata(wikidata_id)
            log.debug("Creating wikidata source concept",
                     wikidata_id=wikidata_id)
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
            lcsh_source_concept = SourceConcept.nodes.get_or_none(
                source_id=lcsh_id, source="lcsh"
            )
            if not lcsh_source_concept:
                concept_lcsh_data = get_lcsh_data(lcsh_id)
                log.debug("Creating lcsh source concept", lcsh_id=lcsh_id)
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
            mesh_source_concept = SourceConcept.nodes.get_or_none(
                source_id=mesh_id, source="mesh"
            )
            if not mesh_source_concept:
                concept_mesh_data = get_mesh_data(mesh_id)
                log.debug("Creating mesh source concept", mesh_id=mesh_id)
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
        for source_concept in self.sources.all():
            if source_concept.source == "wikidata":
                self._get_wikidata_neighbours(
                    source_id=source_concept.source_id
                )
            elif source_concept.source == "lcsh":
                self._get_lcsh_neighbours(source_id=source_concept.source_id)
            elif source_concept.source == "mesh":
                self._get_mesh_neighbours(source_id=source_concept.source_id)

    def _get_wikidata_neighbours(self, source_id):
        log.debug("Getting neighbours from wikidata", source_id=source_id)
        wikidata = get_wikidata(source_id)
        claims = [
            "P31",  # instance of
            "P279",  # subclass of
            "P361",  # part of
            "P527",  # has part
            "P1542",  # has effect
        ]
        related_ids = []
        for claim_id in claims:
            if claim_id in wikidata["claims"]:
                related_ids.extend([
                    related_claim["mainsnak"]["datavalue"]["value"]["id"]
                    for related_claim in wikidata["claims"][claim_id]
                ])

        for wikidata_id in related_ids:
            concept_wikidata = get_wikidata(wikidata_id)
            neighbour_source_concept = SourceConcept.nodes.get_or_none(
                source_id=wikidata_id
            )
            if neighbour_source_concept:
                neighbour_concept = neighbour_source_concept.parent.all()[0]
            else:
                log.debug('Creating neighbour concept', wikidata_id=wikidata_id)
                neighbour_concept = Concept(
                    name=get_wikidata_preferred_name(concept_wikidata)
                ).save()
            log.debug(
                'Connecting neighbour',
                concept_name=self.name,
                neighbour_name=neighbour_concept.name,
            )
            self.neighbours.connect(neighbour_concept)
            neighbour_concept.enrich(wikidata_id=wikidata_id)

    def _get_lcsh_neighbours(self, source_id):
        pass

    def _get_mesh_neighbours(self, source_id):
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
