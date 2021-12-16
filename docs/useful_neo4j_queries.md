# Useful neo4j queries

## Fetch 1000 random relationships

```
MATCH p=()-->() WITH p, rand() AS r ORDER BY r RETURN p LIMIT 1000
```

## Count the stories

```
MATCH (n:Story) RETURN count(n) as count
```