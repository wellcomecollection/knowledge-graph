# Concepts

Enriching the concepts in the catalogue API.

## Why

- Short term goal is to improve search relevance.
- Long term goal is to build an underlying knowledge graph for the collection so that we can improve search relevance.

## What

Working towards something like this (?)

![](architecture.png)

## Populating the graph store with enriched concepts

To kick off the enrichment pipeline, run

```
make populate
```

This cleans the repo, lints the code, runs the tests, and then starts up:

- an enricher, which takes identifiers from known controlled vocabularies and returns additional information (variant names, etc).
- a little ETL pipeline from an ES index to a graph store in neo4j aura. if concepts in the ES index contain identifiers from our set of known controlled vocabularies, they're enriched by the API.

For now, this just bootstraps the graph store from the existing concepts index in the reporting elasticsearch cluster, ie it doesn't work off any of the real pipeline topics/queues.  
The interface to the enricher is currently a REST API and the interface to the graph store is currently a CLI. These components will probably be combined into a more coherent system which might run in a lambda, or similar.

## Tests

To run the tests, run

```
make test
```

To run the pipeline without running the test container first, run

```
make populate--no-tests
```

## Querying the populated graph store

Use the query api to search the existing concepts and return their variant names. Run

```
make api
```

## Graph structure

More detail on the internal structure of the graph store [here](graph_structure.md).
