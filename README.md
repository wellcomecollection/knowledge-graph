# 🕸️ Knowledge Graph

We want to improve the experience of searching, exploring and discovering new material on [wellcomecollection.org](https://wellcomecollection.org). To do that, we're enriching our catalogue with data from external sources and constructing a knowledge graph for the collection.

This repo contains a set of prototype pipelines and search services which allow us to test how this approach might affect the experience of exploring the collection.

## What's a concept?

Works can be tagged with subjects, contributors, genres, languages, etc. Any of these taggable entities which are not works themselves should be considered a concept.

## What's enrichment?

Currently, we're ingesting and connecting data from [LCSH](https://en.m.wikipedia.org/wiki/Library_of_Congress_Subject_Headings), [MeSH](https://en.m.wikipedia.org/wiki/Medical_Subject_Headings), and [wikidata](https://en.m.wikipedia.org/wiki/Wikidata) to enrich concepts. These provide us with variant names, descriptions, useful dates, and connections to neighbouring concepts, among other things.
By incorporating these sources, we can demonstrate a deeper understanding of each concept and provide a richer experience when exploring the collection online.

## What's a knowledge graph?

A map of all the connections between concepts and works.

## Further info

See the [docs folder](/docs) for more information about the project architecture, running the pipeline/UI/graph store locally, etc.
