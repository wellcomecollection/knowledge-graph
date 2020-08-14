# Concepts

Looking into concepts within the catalogue API.

## Populating the graph store with enriched concepts

```
docker-compose up --build
```

This starts up:

- an enricher API, which takes identifiers from known controlled vocabularies and returns additional information (variant names, etc)
- a little ETL pipeline from an ES index to a graph store in neo4j aura. if concepts in the ES index contain identifiers from our set of known controlled vocabularies, they're enriched by the API
