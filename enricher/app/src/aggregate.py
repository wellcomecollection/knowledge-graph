from weco_datascience.logging import get_logger

from .library_of_congress import get_lc_names_data, get_lc_subjects_data
from .mesh import get_mesh_data
from .node import Node
from .utils import (get_unknown_label_data, loc_id_to_wikidata_id,
                    mesh_id_to_wikidata_id, unknown_label_to_wikidata_id,
                    wikidata_id_to_alt_source_ids)
from .wikidata import get_wikidata_data

log = get_logger(__name__)

THIRD_PARTIES = (
    ("lc_subjects", get_lc_subjects_data, loc_id_to_wikidata_id),
    ("lc_names", get_lc_names_data, loc_id_to_wikidata_id),
    ("mesh", get_mesh_data, mesh_id_to_wikidata_id),
    ("unknown", get_unknown_label_data, unknown_label_to_wikidata_id),
)


async def aggregate_wikidata(wikidata_id, label_type="wikidata"):
    wikidata = Node(label=wikidata_id, label_type="wikidata_id")
    response = await get_wikidata_data(wikidata_id)
    variant_names = response["variants"] + [response["title"]]
    for variant in variant_names:
        wikidata.add_child(variant)

    alt_source_ids = await wikidata_id_to_alt_source_ids(wikidata_id)

    for third_party_label_type, get_data, _ in THIRD_PARTIES:
        if (
            alt_source_ids[third_party_label_type]
            and third_party_label_type != label_type
        ):
            children = Node(
                label=alt_source_ids[third_party_label_type],
                label_type=third_party_label_type + "_id",
            )
            response = await get_data(alt_source_ids[third_party_label_type])
            variant_names = response["variants"] + [response["title"]]
            for variant in variant_names:
                children.add_child(variant)

            wikidata.add_child(children)

    return wikidata


async def aggregate(label, label_type):
    enriched_concept = Node(label, label_type)

    if label_type == "wikidata":
        enriched_concept = await aggregate_wikidata(label)

    else:
        for third_party_label_type, get_data, wiki_conversion in THIRD_PARTIES:
            if third_party_label_type == label_type:
                response = await get_data(label)
                variant_names = response["variants"] + [response["title"]]
                for variant in variant_names:
                    enriched_concept.add_child(variant)

                wikidata_id = await wiki_conversion(label)
                if wikidata_id:
                    wikidata = await aggregate_wikidata(wikidata_id, label_type)
                    enriched_concept.add_child(wikidata)

    return enriched_concept
