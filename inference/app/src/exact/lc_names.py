import os
import requests


def get_lc_names_api_response(lc_names_id):
    url = f"http://id.loc.gov/authorities/names/{lc_names_id}.json"
    api_response = requests.get(url)
    if api_response.status_code == 200:
        return api_response.json()
    elif api_response.status_code == 404:
        raise ValueError(f"{lc_names_id} is not a valid lc_names_id")
    else:
        raise ValueError(
            f"something unexpected happened when calling url: {url}"
        )


def get_lc_names_preferred_label(api_response):
    preferred_label_id = "http://www.w3.org/2004/02/skos/core#prefLabel"
    preferred_label = None
    for element in api_response:
        if preferred_label_id in element:
            preferred_label = element[preferred_label_id][0]["@value"]
    return preferred_label


def get_lc_names_variants(api_response):
    variant_id = "http://www.loc.gov/mads/rdf/v1#variantLabel"
    variants = [
        element[variant_id][0]["@value"]
        for element in api_response
        if variant_id in element
    ]
    return variants


def get_lc_names_data(lc_names_id):
    api_response = get_lc_names_api_response(lc_names_id)
    preferred_label = get_lc_names_preferred_label(api_response)
    variants = get_lc_names_variants(api_response)
    return {
        "id": lc_names_id,
        "title": preferred_label,
        "variants": variants
    }
