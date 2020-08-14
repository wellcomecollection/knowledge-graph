import requests


def enrich(authority, authority_id):
    response = requests.get(
        f"http://enricher:80/{authority}/{authority_id}"
    ).json()
    return response
