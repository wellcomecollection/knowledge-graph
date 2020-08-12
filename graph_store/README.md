# Graph Store

## Running

To start populating the graph store, run:

```
docker-compose up --build graph_store
```

The default command is set (and can be changed) in `docker-compose.yml`.

The list of available commands is determined by `graph_store.py`, which can also be viewed via the cli by running:

```
python graph_store.py --help
```
