# Architecture

![architecture](./architecture.png)

1. Works (from stories and collection) are brought into the graph store with their concepts, enriched by third party sources
2. Concepts' neighbours are then fetched from those third party sources, and added to the graph in the same way
3. Works and concepts in the graph are then formatted for elasticsearch, with all of the relevant information from the preferred sources etc, and structured for search performance
4. The UI (hosted on vercel) queries the elasticsearch index to provide search results
