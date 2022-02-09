# Developing / running this code locally


## Pipeline

To run the complete pipeline from end-to-end, run:

```sh
docker-compose up --build pipeline
```

This bundles three scripts together. To run them individually, run:

```sh
docker-compose up --build graph  # establishes the core graph structure
docker-compose up --build neighbours  # adds the neighbour relationships between concepts
docker-compose up --build reindex  # reindexes the graph into a flat elasticsearch structure
```

## Search UI

Navigate to the [search directory](/search/), then

- Run `yarn` to install dependencies.
- Run `yarn env` to link your local repo to the project on vercel and populate a local `.env` file with dev versions of all of the project's secrets.
- Finally, run `yarn dev` to get a local version of the site running.

## Neo4j browser

Useful for exploring data.

```sh
docker compose up --build neo4j
```

## Get a dump of a local neo4j database

```sh
docker compose run neo4j bin/neo4j-admin dump --to=/dump
```
