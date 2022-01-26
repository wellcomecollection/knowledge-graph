# Pipelines

- Ingests and enriches works and stories data as a **neo4j graph** with relationships modeled between:
  - works
    - including different work types, like stories
  - concepts
    - including people, languages
- Creates flat, searchable **elasticsearch indices** for
  - concepts
  - people
  - works
  - stories
