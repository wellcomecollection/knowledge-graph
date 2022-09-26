# Useful neo4j queries

## Increase the limit on the number of nodes displayed by the neo4j browser

Default is 1000 (?)

```
:config initialNodeDisplay: 2500
```

## Fetch 1000 random relationships

```
MATCH p=()-->() WITH p, rand() AS r ORDER BY r RETURN p LIMIT 1000
```

## Count the works

```
MATCH (n:Work {type: "work"}) RETURN count(n) as count
```

## Get subset of relationship types

```
MATCH p=()-[r:CONTRIBUTED_TO|HAS_CONCEPT]->() WITH p, rand() AS r ORDER BY r RETURN p LIMIT 1000
```

## Get nodes within a certain distance of a node

```
MATCH (n {name: 'pain'})
CALL apoc.path.spanningTree(n, 
    {
        maxLevel: 3,
        relationshipFilter: "HAS_NEIGHBOUR|HAS_CONCEPT|CONTRIBUTED_TO"
    }
) YIELD path
RETURN path
```

## Filter for particular node/edge properties

```
match (n:Concept)-[k:HAS_SOURCE_CONCEPT]->(f)
where ((n.name contains ' - ') AND (f.source_type = 'nlm-mesh'))
return n, f
```

## Create a GDS graph of concepts

```
CALL gds.graph.create.cypher(
  'concepts',
  'MATCH (n:Concept) RETURN id(n) AS id',
  'MATCH (n:Concept)-[r:HAS_NEIGHBOUR]->(m:Concept) RETURN id(n) AS source, id(m) AS target')
YIELD
  graphName AS graph, nodeQuery, nodeCount AS nodes, relationshipQuery, relationshipCount AS rels
```

## Determine the degree of every node in the graph

```
CALL gds.degree.stats('concepts')
YIELD centralityDistribution
```

## Measure the centrality of nodes in a graph

```
CALL gds.pageRank.stream(
  'concepts', 
  {
    maxIterations: 20,
    dampingFactor: 0.85
  }
)
YIELD nodeId, score
RETURN gds.util.asNode(nodeId).name AS name, score
ORDER BY score DESC, name ASC
```

## concepts graph with only work-attached concepts

```
MATCH (w:Work)-[]-(c:Concept)-[r:HAS_NEIGHBOUR]-(:Concept) RETURN c
```

which only come from wikidata

```
MATCH (w:Work)-[]-(c:Concept)-[r:HAS_NEIGHBOUR {source:"wikidata"}]-(:Concept) RETURN c
```

## SourceConcepts from wikipedia

```
MATCH (c:Concept)-[r:HAS_SOURCE_CONCEPT]->(s:SourceConcept {source_type:"wikipedia"}) RETURN s
```

## tail the most recent log file

```sh
tail -f data/logs/$(ls -Art data/logs/ | tail -n 1)
```

## Delete all nodes and relationships in a large graph db

```
call apoc.periodic.iterate("MATCH (n) return id(n) as id", "MATCH (n) WHERE id(n) = id DETACH DELETE n", {batchSize:10000})
yield batches, total return batches, total
```
