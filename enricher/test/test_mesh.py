import pytest
from weco_datascience.http import (
    close_persistent_client_session,
    start_persistent_client_session,
)

from enricher.app.src.mesh import (
    get_description,
    get_mesh_data,
    get_title,
    get_variants,
)

from . import mesh_id, mesh_response


@pytest.mark.asyncio
async def test_get_lc_names_data():
    start_persistent_client_session()
    data = await get_mesh_data(mesh_id)
    await close_persistent_client_session()
    assert data


@pytest.mark.asyncio
async def test_get_mesh_data_fails_invalid_id():
    start_persistent_client_session()
    with pytest.raises(ValueError):
        await get_mesh_data("not a valid id")
    await close_persistent_client_session()


def test_get_title():
    title = get_title(mesh_response)
    assert title == "Hemorrhagic Fever, Ebola"


def test_get_description():
    description = get_description(mesh_response)
    assert description == (
        "A highly fatal, acute hemorrhagic fever caused by EBOLAVIRUS."
    )


def test_get_variants():
    variants = get_variants(mesh_response)
    assert set(variants) == set(
        [
            "Ebola Hemorrhagic Fever",
            "Ebola Infection",
            "Ebola Virus Disease",
            "Ebola Virus Infection",
            "Ebolavirus Infection",
            "Hemorrhagic Fever, Ebola",
            "Ebolavirus Infections",
            "Infection, Ebola",
            "Infection, Ebola Virus",
            "Infection, Ebolavirus",
            "Infections, Ebolavirus",
            "Virus Infection, Ebola",
        ]
    )
