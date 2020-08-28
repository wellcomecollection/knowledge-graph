import requests


def get_enriched_concept(authority, authority_id):
    response = requests.get(f"http://enricher:80/{authority}/{authority_id}")
    if response.status_code == 200:
        return response.json()
    else:
        return {"label": authority_id, "label_type": authority, "children": []}


def traverse(node, parent=None):
    """
    recursively yields each node in a tree alongside its parent node (if the
    parent exists)
    """
    yield {
        "parent": parent,
        "child": {"label": node["label"], "label_type": node["label_type"]},
    }

    if node["children"]:
        for child in node["children"]:
            parent = {"label": node["label"], "label_type": node["label_type"]}
            yield from traverse(child, parent)
