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

from . import (
    get_loc_data,
    get_loc_id_from_wikidata,
    get_loc_preferred_label,
    get_loc_variant_labels,
    get_logger,
    get_mesh_data,
    get_mesh_description,
    get_mesh_id_from_wikidata,
    get_mesh_preferred_concept_data,
    get_mesh_preferred_label,
    get_wikidata,
    get_wikidata_description,
    get_wikidata_id_from_loc_data,
    get_wikidata_preferred_label,
    get_wikidata_variant_labels,
)

log = get_logger(__name__)


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


class Work(StructuredNode):
    uid = UniqueIdProperty()
    wellcome_id = StringProperty(unique_index=True, required=True)
    title = StringProperty(required=True)
    concepts = RelationshipFrom("Concept", "HAS_CONCEPT")
    contributors = RelationshipFrom("Concept", "CONTRIBUTED_TO")
    wikidata_id = StringProperty(unique_index=True)
    type = StringProperty(
        required=True,
        choices={c: c for c in ["story", "work"]},
    )
    format = StringProperty()
    published = StringProperty()


class SourceConcept(StructuredNode):
    uid = UniqueIdProperty()
    source_id = StringProperty(unique_index=True, required=True)
    source_type = StringProperty(
        required=True,
        choices={
            c: c
            for c in [
                "wikidata",
                "lc-subjects",
                "lc-names",
                "nlm-mesh",
                "label-derived",
            ]
        },
    )
    description = StringProperty()
    preferred_label = StringProperty()
    variant_labels = ArrayProperty(StringProperty())
    parent = RelationshipFrom("Concept", "HAS_SOURCE_CONCEPT")


class Concept(StructuredNode):
    label = StringProperty(required=True)
    uid = UniqueIdProperty()
    wellcome_id = StringProperty(unique_index=True)
    sources = RelationshipTo("SourceConcept", "HAS_SOURCE_CONCEPT")
    works = RelationshipTo("Work", "HAS_CONCEPT")
    neighbours = Relationship("Concept", "HAS_NEIGHBOUR")
    contributed_to_work = RelationshipTo("Work", "CONTRIBUTED_TO")
    type = StringProperty(
        default="subject",
        choices={c: c for c in ["subject", "person"]},
    )

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
        if source_type == "label-derived":
            self._connect_label_derived_source(source_id)

    def _connect_label_derived_source(self, source_id):
        try:
            source_concept = SourceConcept.nodes.get_or_none(
                source_id=source_id, source_type="label-derived"
            )
            if not source_concept:
                log.debug(
                    "Creating source concept",
                    source_id=source_id,
                    source_type="label-derived",
                )
                source_concept = SourceConcept(
                    source_id=source_id,
                    source_type="label-derived",
                    preferred_label=self.label,
                    variant_labels=[],
                ).save()
            if not self.sources.is_connected(source_concept):
                log.debug(
                    "Connecting source concept",
                    concept=self.label,
                    source_id=source_id,
                    source_type="label-derived",
                )
                self.sources.connect(source_concept)
        except (ValueError) as error:
            log.exception(
                f"Error connecting label-derived source concept",
                concept=self.label,
                loc_id=source_id,
                error=error,
            )

    def _connect_wikidata_source(self, wikidata_id, get_linked_schemes=[]):
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
                preferred_label=get_wikidata_preferred_label(source_data),
                variant_labels=get_wikidata_variant_labels(source_data),
            ).save()
        if not self.sources.is_connected(source_concept):
            log.debug(
                "Connecting wikidata source concept",
                concept=self.label,
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
        self, source_id, source_type, get_linked_schemes=[]
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
                    preferred_label=get_loc_preferred_label(loc_data),
                    variant_labels=get_loc_variant_labels(loc_data),
                ).save()
            if not self.sources.is_connected(source_concept):
                log.debug(
                    "Connecting source concept",
                    concept=self.label,
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
        except (ValueError) as error:
            log.exception(
                f"Error connecting {source_type} source concept",
                concept=self.label,
                loc_id=source_id,
                error=error,
            )

    def _connect_mesh_source(self, mesh_id):
        try:
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
                    preferred_label=get_mesh_preferred_label(source_data),
                    variant_labels=[],
                ).save()
            if not self.sources.is_connected(source_concept):
                log.debug(
                    "Connecting mesh source concept",
                    concept=self.label,
                    mesh_id=mesh_id,
                )
                self.sources.connect(source_concept)
        except (ValueError) as error:
            log.exception(
                "Error connecting mesh source concept",
                concept=self.label,
                loc_id=mesh_id,
                error=error,
            )

    def get_neighbours(self):
        log.info("Getting neighbours for concept", concept=self.label)
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
            "P460",  # said to be the same as
            "P2579",  # studied by
        ]
        related_ids = []
        for claim_id in claims:
            try:
                if claim_id in wikidata["claims"]:
                    related_ids.extend(
                        [
                            related_claim["mainsnak"]["datavalue"]["value"][
                                "id"
                            ]
                            for related_claim in wikidata["claims"][claim_id]
                        ]
                    )
            except (KeyError, TypeError):
                continue
        for neighbour_wikidata_id in related_ids:
            log.debug(
                "Found related wikidata id", wikidata_id=neighbour_wikidata_id
            )
            neighbour_source_concept = SourceConcept.nodes.get_or_none(
                source_id=neighbour_wikidata_id, source_type="wikidata"
            )
            if neighbour_source_concept:
                log.debug(
                    "Found existing wikidata neighbour source concept",
                    wikidata_id=neighbour_wikidata_id,
                )
                neighbour_concept = neighbour_source_concept.parent.all()[0]
            else:
                try:
                    neighbour_concept_wikidata = get_wikidata(
                        neighbour_wikidata_id
                    )
                    label = get_wikidata_preferred_label(
                        neighbour_concept_wikidata
                    )
                    log.info(
                        "Creating neighbour concept",
                        wikidata_id=neighbour_wikidata_id,
                        label=label,
                    )
                    neighbour_concept = Concept(label=label).save()
                    neighbour_concept.collect_sources(
                        source_id=neighbour_wikidata_id, source_type="wikidata"
                    )
                except ValueError as error:
                    log.exception(
                        "Skipping neighbour, no data found",
                        wikidata_id=neighbour_wikidata_id,
                        message=error,
                    )
                    continue

            if neighbour_concept == self:
                log.debug(
                    "Skipping neighbour, concept is the same",
                    concept_label=self.label,
                    neighbour_label=neighbour_concept.label,
                )
                continue
            else:
                log.debug(
                    "Connecting neighbour",
                    concept_label=self.label,
                    neighbour_label=neighbour_concept.label,
                )
                self.neighbours.connect(neighbour_concept)

    def _get_loc_neighbours(self, source_id):
        loc_data = get_loc_data(source_id)
        related_ids = []
        keys = [
            "http://www.w3.org/2004/02/skos/core#broader",
            "http://www.w3.org/2004/02/skos/core#narrower",
        ]
        for key in keys:
            if key in loc_data:
                related_ids.extend(
                    [Path(authority["@id"]).name for authority in loc_data[key]]
                )
        if "http://www.loc.gov/mads/rdf/v1#componentList" in loc_data:
            related_ids.extend(
                [
                    Path(component["@id"]).name
                    for component in loc_data[
                        "http://www.loc.gov/mads/rdf/v1#componentList"
                    ][0]["@list"]
                ]
            )

        for neighbour_loc_id in related_ids:
            log.debug("Found related loc id", loc_id=neighbour_loc_id)
            neighbour_source_concept = SourceConcept.nodes.get_or_none(
                source_id=neighbour_loc_id
            )
            if neighbour_source_concept:
                log.debug(
                    "Found existing neighbour source concept",
                    loc_id=neighbour_loc_id,
                )
                neighbour_concept = neighbour_source_concept.parent.all()[0]
            else:
                try:
                    neighbour_concept_loc_data = get_loc_data(neighbour_loc_id)
                    label = get_loc_preferred_label(neighbour_concept_loc_data)
                    log.info(
                        "Creating neighbour concept",
                        loc_id=neighbour_loc_id,
                        label=label,
                    )
                    neighbour_concept = Concept(label=label).save()
                    neighbour_concept.collect_sources(
                        source_id=neighbour_loc_id,
                        source_type=(
                            "lc-subjects"
                            if neighbour_loc_id.startswith("s")
                            else "lc-names"
                        ),
                    )
                except (ValueError) as error:
                    log.exception(
                        "Skipping neighbour, no data found",
                        neighbour_loc_id=neighbour_loc_id,
                        message=error,
                    )
                    continue

            if neighbour_concept == self:
                log.debug(
                    "Skipping neighbour, concept is the same",
                    concept_label=self.label,
                    neighbour_label=neighbour_concept.label,
                )
                continue
            else:
                log.debug(
                    "Connecting neighbour",
                    concept_label=self.label,
                    neighbour_label=neighbour_concept.label,
                )
                self.neighbours.connect(neighbour_concept)

    def _get_mesh_neighbours(self, mesh_id):
        try:
            mesh_data = get_mesh_data(mesh_id)
            related_ids = []
            keys = [
                "seeAlso",
                "hasDescriptor",
                "hasQualifier",
                "broaderDescriptor",
                "broaderQualifier",
            ]
            for key in keys:
                if key in mesh_data:
                    if isinstance(mesh_data[key], list):
                        related_ids.extend(
                            [Path(related).name for related in mesh_data[key]]
                        )
                    elif isinstance(mesh_data[key], str):
                        related_ids.append(Path(mesh_data[key]).name)

            for neighbour_mesh_id in related_ids:
                log.debug("Found related mesh id", mesh_id=neighbour_mesh_id)
                neighbour_source_concept = SourceConcept.nodes.get_or_none(
                    source_id=neighbour_mesh_id, source_type="nlm-mesh"
                )
                if neighbour_source_concept:
                    log.debug(
                        "Found existing mesh neighbour source concept",
                        mesh_id=neighbour_mesh_id,
                    )
                    neighbour_concept = neighbour_source_concept.parent.all()[0]
                else:
                    try:
                        neighbour_concept_mesh_data = get_mesh_data(
                            neighbour_mesh_id
                        )
                        label = get_mesh_preferred_label(
                            neighbour_concept_mesh_data
                        )
                        log.info(
                            "Creating neighbour concept",
                            mesh_id=neighbour_mesh_id,
                            label=label,
                        )
                        neighbour_concept = Concept(label=label).save()
                        neighbour_concept.collect_sources(
                            source_id=neighbour_mesh_id, source_type="nlm-mesh"
                        )
                    except ValueError as error:
                        log.exception(
                            "Skipping neighbour, no data found",
                            neighbour_mesh_id=neighbour_mesh_id,
                            message=error,
                        )
                        continue

                if neighbour_concept == self:
                    log.debug(
                        "Skipping neighbour, concept is the same",
                        concept_label=self.label,
                        neighbour_label=neighbour_concept.label,
                    )
                    continue
                else:
                    log.debug(
                        "Connecting neighbour",
                        concept_label=self.label,
                        neighbour_label=neighbour_concept.label,
                    )
                    self.neighbours.connect(neighbour_concept)
        except TypeError as error:
            log.error(
                "Error getting mesh neighbours",
                mesh_id=mesh_id,
                error=error,
            )
