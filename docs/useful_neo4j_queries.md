# Useful neo4j queries

## Fetch 1000 random relationships

```
MATCH p=()-->() WITH p, rand() AS r ORDER BY r RETURN p LIMIT 1000
```

## Count the works

```
MATCH (n:Work) RETURN count(n) as count
```

## Get subset of relationship types

```
MATCH p=()-[r:CONTRIBUTED_TO|HAS_CONCEPT]->() WITH p, rand() AS r ORDER BY r RETURN p LIMIT 1000
```
