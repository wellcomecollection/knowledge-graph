import json
import requests


def get_enriched_concept(authority, authority_id):
    return requests.get(
        f"http://enricher:80/{authority}/{authority_id}"
    ).json()


def traverse(node, parent=None):
    """
    recursively yields each node in a tree alongside its parent node (if the 
    parent exists)
    """
    yield {
        "parent": parent,
        "child": {
            "label": node["label"],
            "label_type": node["label_type"]
        }
    }

    if node["children"]:
        for child in node["children"]:
            parent = {
                "label": node["label"],
                "label_type": node["label_type"]
            }
            yield from traverse(child, parent)
