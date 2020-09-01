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

from . import lc_names_id, lc_subjects_id, lc_subjects_response


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
    wikidata_id = get_wikidata_id(lc_subjects_response)
    assert wikidata_id == "Q1420"


def test_get_variants():
    variants = get_variants(lc_subjects_response)
    assert set(variants) == set(
        [
            "Autos (Automobiles)",
            "Cars (Automobiles)",
            "Gasoline automobiles",
            "Motorcars (Automobiles)",
        ]
    )


def test_get_label():
    label = get_label(lc_subjects_response)
    assert label == "Automobiles"


@pytest.mark.asyncio
async def test_get_hierarchical_concepts():
    start_persistent_client_session()
    broader_concepts = await get_hierarchical_concepts(
        lc_subjects_response, "Broader"
    )
    narrower_concepts = await get_hierarchical_concepts(
        lc_subjects_response, "Narrower"
    )
    assert set(broader_concepts) == set(
        ["Motor vehicles", "Transportation, Automotive"]
    )
    assert set(narrower_concepts) == set(
        [
            "BLMC automobiles",
            "NSU automobile",
            "Hydrogen cars",
            "Architect-designed automobiles",
            "Napier automobiles",
            "Frazer automobile",
            "Wanderer automobile",
            "Isetta automobile",
            "Sports cars",
            "Pegaso automobile",
            "Lancia automobile",
            "Moskvich automobile",
            "Fiat automobiles",
            "Horch automobile",
            "Bridgwater automobile",
            "Kia automobiles",
            "Marino automobiles",
            "DKW automobile",
            "Tata automobiles",
            "Iso automobiles",
            "Electric automobiles",
            "Microcars",
            "Honda automobile",
            "Railton automobile",
            "Haynes automobile",
            "Daihatsu automobiles",
            "Audi automobile",
            "General Motors automobiles",
            "KamAZ automobile",
            "Reliant automobile",
            "Zastava automobile",
            "Jensen automobile",
            "Isotta-Fraschini automobile",
            "Freikaiserwagen automobile",
            "Peugeot automobile",
            "Aston Martin automobile",
            "Duryea automobile",
            "Seat automobiles",
            "ARO automobile",
            "Pierce-Arrow automobile",
            "Volkswagen automobiles",
            "Puch automobiles",
            "Stutz automobile",
            "Vanden Plas automobile",
            "Toyota automobiles",
            "Lea-Francis automobile",
            "Suzuki automobile",
            "Jowett automobile",
            "Ferrari automobile",
            "Elcar automobile",
            "Holsman automobile",
            "Brough Superior automobile",
            "Facel Vega automobile",
            "Alpina automobiles",
            "Autobianchi automobiles",
            "Syrena automobile",
            "Citroën automobile",
            "Bristol automobile",
            "Jaguar automobile",
            "Alfa Romeo automobile",
            "Brewster automobiles",
            "Amilcar automobiles",
            "Graham-Paige automobiles",
            "Tucker automobile",
            "Lexington automobiles",
            "Adler Trumpf-Junior automobile",
            "Bucciali automobile",
            "American Bantam automobile",
            "Isuzu automobile",
            "Muscle cars",
            "Experimental automobiles",
            "Rolls-Royce automobile",
            "Glas automobile",
            "Nash automobiles",
            "Mitchell automobiles",
            "Bugatti automobile",
            "Panhard automobile",
            "Holden automobiles",
            "OM automobiles",
            "Hispano-Suiza automobile",
            "Allard automobile",
            "Presidential automobiles",
            "Subaru automobile",
            "Proton automobile",
            "Simca automobiles",
            "Volga automobile",
            "Frazer Nash automobile",
            "Bianchi automobiles",
            "Pobeda automobile",
            "Burney Streamline automobile",
            "Shelby automobile",
            "Marmon automobile",
            "Auburn automobile",
            "Lanchester automobiles",
            "Pratt-Elkhart automobile",
            "Polonez automobile",
            "Škoda automobile",
            "Lotus automobiles",
            "Jordan automobile",
            "Wolseley automobile",
            "Borgward automobile",
            "Kaiser automobile",
            "Niva automobile",
            "Nissan automobile",
            "Hupp automobile",
            "Tatra automobile",
            "Hyundai automobile",
            "Used cars",
            "Porsche automobiles",
            "Rental automobiles",
            "Rover automobiles",
            "Pullman automobile",
            "Mazda automobile",
            "Dagmar automobile",
            "Standard automobile",
            "Innocenti automobiles",
            "BMW automobiles",
            "Peerless automobile",
            "Zaporozhets automobile",
            "Daf automobile",
            "Vauxhall automobile",
            "Salmson automobile",
            "Ford automobile",
            "EMW automobile",
            "Hino automobile",
            "Dacia automobile",
            "Cleveland automobiles",
            "Checker automobiles",
            "Winton automobiles",
            "Spyker automobiles",
            "W Motors automobiles",
            "Bentley automobile",
            "Pilain automobiles",
            "Gordon-Keeble automobiles",
            "Ural automobile",
            "Delage automobile",
            "Duesenberg automobile",
            "Chaĭka automobile",
            "Morgan automobile",
            "Berliet automobiles",
            "Photography of automobiles",
            "American Motors automobiles",
            "Daimler automobile",
            "Lola automobiles",
            "McFarlan automobile",
            "Chandler automobile",
            "Abarth automobiles",
            "Limousines",
            "Talbot automobiles",
            "Triumph automobile",
            "Locomobile automobile",
            "Cord automobile",
            "Packard automobile",
            "Alvis automobile",
            "De Dion-Bouton automobile",
            "Stoewer automobile",
            "Hindustan Ambassador automobile",
            "Wartburg automobile",
            "Bricklin automobile",
            "Renault automobile",
            "Willys automobiles",
            "Trabant automobile",
            "Saab automobile",
            "Durant Motors automobiles",
            "Franklin automobile",
            "Mitsubishi automobiles",
            "Antique and classic cars",
            "Opel automobile",
            "Maserati automobiles",
            "Lamborghini automobile",
            "Ssangyong automobile",
            "Rootes automobiles",
            "Rosengart automobiles",
            "Studebaker automobile",
            "Delahaye automobile",
            "Maybach automobile",
            "Volvo automobile",
            "DaimlerChrysler automobiles",
            "Compact cars",
            "Devrim automobile",
            "Station wagons",
            "Diesel automobiles",
            "Messerschmitt automobiles",
            "Cameron automobile",
            "Diatto automobiles",
            "A.C. automobile",
            "Cisitalia automobiles",
            "Oakland automobile",
        ]
    )
    await close_persistent_client_session()
