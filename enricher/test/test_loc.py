import pytest
from weco_datascience.http import (
    close_persistent_client_session,
    start_persistent_client_session,
)

from enricher.app.src.library_of_congress import (
    get_hierarchical_concepts,
    get_label,
    get_lc_names_data,
    get_lc_subjects_data,
    get_variants,
    get_wikidata_id,
)

from . import lc_names_id, lc_subjects_id, loc_response


@pytest.mark.asyncio
async def test_get_lc_names_data():
    start_persistent_client_session()
    data = await get_lc_names_data(lc_names_id)
    await close_persistent_client_session()
    assert data


@pytest.mark.asyncio
async def test_get_lc_subjects_data():
    start_persistent_client_session()
    data = await get_lc_subjects_data(lc_subjects_id)
    await close_persistent_client_session()
    assert data


@pytest.mark.asyncio
async def test_get_lc_subjects_data_fails_invalid_id():
    start_persistent_client_session()
    with pytest.raises(ValueError):
        await get_lc_subjects_data("not a valid id")
    await close_persistent_client_session()


@pytest.mark.asyncio
async def test_get_lc_names_data_fails_invalid_id():
    start_persistent_client_session()
    with pytest.raises(ValueError):
        await get_lc_names_data("not a valid id")
    await close_persistent_client_session()


def test_get_wikidata_id():
    wikidata_id = get_wikidata_id(loc_response)
    assert wikidata_id == "Q1420"


def test_get_variants():
    variants = get_variants(loc_response)
    assert set(variants) == set(
        [
            "Autos (Automobiles)",
            "Cars (Automobiles)",
            "Gasoline automobiles",
            "Motorcars (Automobiles)",
        ]
    )


def test_get_label():
    label = get_label(loc_response)
    assert label == "Automobiles"


@pytest.mark.asyncio
async def test_get_hierarchical_concepts():
    start_persistent_client_session()
    broader_concepts = await get_hierarchical_concepts(loc_response, "Broader")
    narrower_concepts = await get_hierarchical_concepts(
        loc_response, "Narrower"
    )
    await close_persistent_client_session()
    assert set(broader_concepts) == set(
        ["Motor vehicles", "Transportation, Automotive"]
    )
    assert set(narrower_concepts) == set(["BLMC automobiles", "NSU automobile"])
