# Enricher

This module is where the interesting stuff happens. It's currently build as a REST API, but the whole thing will probably be switched to a lambda fed by a queue, or similar.

The code takes an authoritative ID for a concept and aggregates data from external sources (wikidata, LCSH, lc names, MeSH) before returning a complete set of its variant names.

# Usage

You should be able to hit the API with a variety of types of ID, eg

- `http://localhost/?id_type=wikidata&id=Q42`
- `http://localhost/?id_type=lc-subjects&id=sh90004313`
- `http://localhost/?id_type=lc-names&id=nr91020770`
- `http://localhost/?id_type=mesh&id=D001336`
