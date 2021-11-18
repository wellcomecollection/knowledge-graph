from fastapi import FastAPI, HTTPException
from weco_datascience.http import (close_persistent_client_session,
                                   start_persistent_client_session)
from weco_datascience.logging import get_logger

from .graph import Graph

log = get_logger(__name__)

# initialise the graph object
graph = Graph()

# initialise the API
app = FastAPI(
    title="Graph store querier",
    description="Queries the graph store",
)


@app.get("/")
async def query(query: str):
    try:
        variant_names = graph.search(query)
        log.info(variant_names)
        return {
            "query": query,
            "variant_names": variant_names
        }
    except ValueError as e:
        error_string = str(e)
        log.error(error_string)
        raise HTTPException(status_code=404, detail=error_string)


@app.get("/healthcheck")
def healthcheck():
    return {"status": "healthy"}


@app.on_event("startup")
def on_startup():
    start_persistent_client_session()


@app.on_event("shutdown")
async def on_shutdown():
    await close_persistent_client_session()
