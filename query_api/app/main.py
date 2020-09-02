from fastapi import FastAPI, HTTPException
from weco_datascience.http import (close_persistent_client_session,
                                   start_persistent_client_session)
from weco_datascience.logging import get_logger

log = get_logger(__name__)

# initialise API
app = FastAPI(
    title="Graph store querier",
    description="Queries the graph store",
)


@app.get("/query/{query}")
async def query(query: str):
    if query == "invalid":
        error_string = f"{query} isn't a valid query"
        log.error(error_string)
        raise HTTPException(status_code=404, detail=error_string)

    try:
        return query
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
