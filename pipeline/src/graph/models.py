from pathlib import Path

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
from structlog import get_logger

from . import (
    get_loc_data,
    get_loc_id_from_wikidata,
    get_loc_preferred_name,
    get_loc_variant_names,
    get_mesh_data,
    get_mesh_description,
    get_mesh_id_from_wikidata,
    get_mesh_preferred_concept_data,
    get_mesh_preferred_name,
    get_wikidata,
    get_wikidata_description,
    get_wikidata_id_from_loc_data,
    get_wikidata_preferred_name,
    get_wikidata_variant_names,
)

log = get_logger()


class BaseConcept(StructuredNode):
    name = StringProperty(required=True)
    uid = UniqueIdProperty()
    sources = RelationshipTo("SourceConcept", "HAS_SOURCE_CONCEPT")


class Story(StructuredNode):
    uid = UniqueIdProperty()
    wellcome_id = StringProperty(unique_index=True, required=True)
    published = DateProperty(required=True)
    title = StringProperty(required=True)
    wikidata_id = StringProperty(unique_index=True)
    concepts = RelationshipFrom("Concept", "HAS_CONCEPT")
    contributors = RelationshipFrom("Person", "CONTRIBUTED_TO")


class Work(StructuredNode):
    uid = UniqueIdProperty()
    wellcome_id = StringProperty(unique_index=True, required=True)
    title = StringProperty(required=True)
    concepts = RelationshipFrom("Concept", "HAS_CONCEPT")
    contributors = RelationshipFrom("Person", "CONTRIBUTED_TO")


class SourceConcept(StructuredNode):
    uid = UniqueIdProperty()
    source_id = StringProperty(unique_index=True, required=True)
    source_type = StringProperty(
        required=True,
        choices={
            c: c for c in ["wikidata", "lc-subjects", "lc-names", "nlm-mesh"]
        },
    )
    description = StringProperty()
    preferred_name = StringProperty()
    variant_names = ArrayProperty(StringProperty())
    parent = RelationshipFrom("BaseConcept", "HAS_SOURCE_CONCEPT")


class Concept(BaseConcept):
    stories = RelationshipTo("Story", "HAS_CONCEPT")
    neighbours = Relationship("Concept", "HAS_NEIGHBOUR")

    def collect_sources(self, source_id, source_type):
        if source_type == "wikidata":
            self._connect_wikidata_source(
                source_id,
                get_linked_schemes=["lc-subjects", "lc-names", "nlm-mesh"],
            )
        if source_type.startswith("lc-"):
            self._connect_loc_source(
                source_id,
                source_type=source_type,
                get_linked_schemes=["wikidata"],
            )
        if source_type == "nlm-mesh":
            self._connect_mesh_source(source_id)

    def _connect_wikidata_source(self, wikidata_id, get_linked_schemes=None):
        source_data = get_wikidata(wikidata_id)
        source_concept = SourceConcept.nodes.get_or_none(
            source_id=wikidata_id, source_type="wikidata"
        )
        if not source_concept:
            log.debug(
                "Creating wikidata source concept", wikidata_id=wikidata_id
            )
            source_concept = SourceConcept(
                source_id=wikidata_id,
                source_type="wikidata",
                description=get_wikidata_description(source_data),
                preferred_name=get_wikidata_preferred_name(source_data),
                variant_names=get_wikidata_variant_names(source_data),
            ).save()
        if not self.sources.is_connected(source_concept):
            log.debug(
                "Connecting wikidata source concept",
                concept=self.name,
                wikidata_id=wikidata_id,
            )
            self.sources.connect(source_concept)

        if (
            "lc-subjects" in get_linked_schemes
            or "lc-names" in get_linked_schemes
        ):
            loc_id = get_loc_id_from_wikidata(source_data)
            if loc_id:
                if loc_id.startswith("n"):
                    self._connect_loc_source(
                        source_id=loc_id, source_type="lc-names"
                    )
                if loc_id.startswith("s"):
                    self._connect_loc_source(
                        source_id=loc_id, source_type="lc-subjects"
                    )
        if "nlm-mesh" in get_linked_schemes:
            mesh_id = get_mesh_id_from_wikidata(source_data)
            if mesh_id:
                self._connect_mesh_source(mesh_id)

    def _connect_loc_source(
        self, source_id, source_type, get_linked_schemes=None
    ):
        try:
            loc_data = get_loc_data(source_id)
            source_concept = SourceConcept.nodes.get_or_none(
                source_id=source_id, source_type=source_type
            )
            if not source_concept:
                log.debug(
                    "Creating source concept",
                    source_id=source_id,
                    source_type=source_type,
                )
                source_concept = SourceConcept(
                    source_id=source_id,
                    source_type=source_type,
                    preferred_name=get_loc_preferred_name(loc_data),
                    variant_names=get_loc_variant_names(loc_data),
                ).save()
            if not self.sources.is_connected(source_concept):
                log.debug(
                    "Connecting source concept",
                    concept=self.name,
                    source_id=source_id,
                    source_type=source_type,
                )
                self.sources.connect(source_concept)

            if "wikidata" in get_linked_schemes:
                wikidata_id = get_wikidata_id_from_loc_data(loc_data)
                if wikidata_id:
                    self._connect_wikidata_source(
                        wikidata_id, get_linked_schemes=["nlm-mesh"]
                    )
        except (ValueError) as e:
            log.exception(
                "Error connecting lc-subjects source concept",
                concept=self.name,
                loc_id=source_id,
                error=e,
            )

    def _connect_mesh_source(self, mesh_id):
        source_data = get_mesh_data(mesh_id)
        source_concept = SourceConcept.nodes.get_or_none(
            source_id=mesh_id, source_type="nlm-mesh"
        )
        if not source_concept:
            source_data = get_mesh_preferred_concept_data(source_data)
            log.debug("Creating mesh source concept", mesh_id=mesh_id)
            source_concept = SourceConcept(
                source_id=mesh_id,
                source_type="nlm-mesh",
                description=get_mesh_description(source_data),
                preferred_name=get_mesh_preferred_name(source_data),
                variant_names=[],
            ).save()
        if not self.sources.is_connected(source_concept):
            log.debug(
                "Connecting mesh source concept",
                concept=self.name,
                mesh_id=mesh_id,
            )
            self.sources.connect(source_concept)

    def get_neighbours(self):
        for source_concept in self.sources.all():
            if source_concept.source_type == "wikidata":
                self._get_wikidata_neighbours(
                    wikidata_id=source_concept.source_id
                )
            elif (
                source_concept.source_type == "lc-subjects"
                or source_concept.source_type == "lc-names"
            ):
                self._get_loc_neighbours(
                    source_id=source_concept.source_id,
                    source_type=source_concept.source_type,
                )
            elif source_concept.source_type == "nlm-mesh":
                self._get_mesh_neighbours(mesh_id=source_concept.source_id)

    def _get_wikidata_neighbours(self, wikidata_id):
        log.debug("Getting neighbours from wikidata", source_id=wikidata_id)
        wikidata = get_wikidata(wikidata_id)
        claims = [
            # should probably add more properties to this list
            "P31",  # instance of
            "P279",  # subclass of
            "P361",  # part of
            "P527",  # has part
            "P1542",  # has effect
        ]
        related_ids = []
        for claim_id in claims:
            if claim_id in wikidata["claims"]:
                related_ids.extend(
                    [
                        related_claim["mainsnak"]["datavalue"]["value"]["id"]
                        for related_claim in wikidata["claims"][claim_id]
                    ]
                )
        log.debug("Found related wikidata ids", related_ids=related_ids)
        for wikidata_id in related_ids:
            neighbour_source_concept = SourceConcept.nodes.get_or_none(
                source_id=wikidata_id, source_type="wikidata"
            )
            if neighbour_source_concept:
                log.debug(
                    "Found existing wikidata neighbour source concept",
                    wikidata_id=wikidata_id,
                )
                neighbour_concept = neighbour_source_concept.parent.all()[0]
            else:
                neighbour_concept_wikidata = get_wikidata(wikidata_id)
                name = get_wikidata_preferred_name(neighbour_concept_wikidata)
                log.debug(
                    "Creating neighbour concept",
                    wikidata_id=wikidata_id,
                    name=name,
                )
                neighbour_concept = Concept(
                    name=get_wikidata_preferred_name(neighbour_concept_wikidata)
                ).save()
                neighbour_concept.collect_sources(
                    source_id=wikidata_id, source_type="wikidata"
                )
            log.debug(
                "Connecting neighbour",
                concept_name=self.name,
                neighbour_name=neighbour_concept.name,
            )
            self.neighbours.connect(neighbour_concept)

    def _get_loc_neighbours(self, source_id, source_type):
        loc_data = get_loc_data(source_id)
        key = "http://www.loc.gov/mads/rdf/v1#hasBroaderAuthority"
        if key in loc_data:
            related_ids = [
                Path(authority["@id"]).name for authority in loc_data[key]
            ]
        else:
            related_ids = []
        log.debug("Found related loc ids", related_ids=related_ids)
        for loc_id in related_ids:
            neighbour_source_concept = SourceConcept.nodes.get_or_none(
                source_id=source_id, source_type=source_type
            )
            if neighbour_source_concept:
                log.debug(
                    "Found existing neighbour source concept", loc_id=loc_id,
                )
                neighbour_concept = neighbour_source_concept.parent.all()[0]
            else:
                neighbour_concept_loc_data = get_loc_data(loc_id)
                log.debug("Creating neighbour concept", loc_id=loc_id)
                neighbour_concept = Concept(
                    name=get_loc_preferred_name(neighbour_concept_loc_data)
                ).save()
                neighbour_concept.collect_sources(
                    source_id=loc_id,
                    source_type=(
                        "lc-subjects" if loc_id.startswith("s") else "lc-names"
                    ),
                )
            log.debug(
                "Connecting neighbour",
                concept_name=self.name,
                neighbour_name=neighbour_concept.name,
            )
            self.neighbours.connect(neighbour_concept)

    def _get_mesh_neighbours(self, mesh_id):
        mesh_data = get_mesh_data(mesh_id)
        if "seeAlso" in mesh_data:
            if isinstance(mesh_data["seeAlso"], list):
                related_ids = [
                    Path(related).name for related in mesh_data["seeAlso"]
                ]
            elif isinstance(mesh_data["seeAlso"], str):
                related_ids = [Path(mesh_data["seeAlso"]).name]
            else:
                related_ids = []
        else:
            related_ids = []

        log.debug("Found related mesh ids", related_ids=related_ids)
        for mesh_id in related_ids:
            neighbour_source_concept = SourceConcept.nodes.get_or_none(
                source_id=mesh_id, source_type="nlm-mesh"
            )
            if neighbour_source_concept:
                log.debug(
                    "Found existing mesh neighbour source concept",
                    mesh_id=mesh_id,
                )
                neighbour_concept = neighbour_source_concept.parent.all()[0]
            else:
                neighbour_concept_mesh_data = get_mesh_data(mesh_id)
                log.debug("Creating neighbour concept", mesh_id=mesh_id)
                neighbour_concept = Concept(
                    name=get_mesh_preferred_name(neighbour_concept_mesh_data)
                ).save()
                neighbour_concept.collect_sources(
                    source_id=mesh_id, source_type="nlm-mesh"
                )
            log.debug(
                "Connecting neighbour",
                concept_name=self.name,
                neighbour_name=neighbour_concept.name,
            )
            self.neighbours.connect(neighbour_concept)


class Person(Concept):
    contributed_to_story = RelationshipTo("Story", "CONTRIBUTED_TO")
    contributed_to_work = RelationshipTo("Work", "CONTRIBUTED_TO")
