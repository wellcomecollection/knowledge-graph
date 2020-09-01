import pytest
from weco_datascience.http import (
    close_persistent_client_session,
    start_persistent_client_session,
)

from enricher.app.src.wikidata import get_wikidata_data
from enricher.app.src.wikidata.api import (
    get_birth_date,
    get_broader_concepts,
    get_death_date,
    get_description,
    get_title,
    get_variants,
)

from . import wikidata_id, wikidata_response


@pytest.mark.asyncio
async def test_get_lc_names_data():
    start_persistent_client_session()
    data = await get_wikidata_data(wikidata_id)
    await close_persistent_client_session()
    assert data


@pytest.mark.asyncio
async def test_get_wikidata_data_fails_invalid_id():
    start_persistent_client_session()
    with pytest.raises(ValueError):
        await get_wikidata_data("not a valid id")
    await close_persistent_client_session()


def test_get_birth_date():
    birth_date = get_birth_date(wikidata_response)
    assert birth_date == "+1952-03-11T00:00:00Z"


@pytest.mark.asyncio
async def test_get_broader_concepts():
    start_persistent_client_session()
    broader_concepts = await get_broader_concepts(wikidata_response)
    await close_persistent_client_session()
    assert broader_concepts == ["human"]


def test_get_death_date():
    death_date = get_death_date(wikidata_response)
    assert death_date == "+2001-05-11T00:00:00Z"


def test_get_description():
    description = get_description(wikidata_response)
    assert description == "English writer and humorist"


def test_get_title():
    title = get_title(wikidata_response)
    assert title == "Douglas Adams"


@pytest.mark.asyncio
async def test_get_variants():
    start_persistent_client_session()
    variants = await get_variants(wikidata_response)
    await close_persistent_client_session()
    assert variants == [
        "Douglas Noel Adams",
        "Douglas Noël Adams",
        "Douglas N. Adams",
    ]
