from fastapi import FastAPI, HTTPException

from weco_datascience.http import (
    close_persistent_client_session,
    start_persistent_client_session,
)
from weco_datascience.logging import get_logger

from .src.aggregate import aggregate

log = get_logger(__name__)

# initialise API
app = FastAPI(
    title="Concepts Enricher",
    description="One-stop-shop for enriching concepts with wikidata",
)

valid_id_types = ["lc_names", "lc_subjects", "mesh", "wikidata"]


@app.get("/{id_type}/{id}")
async def query(id_type: str, id: str):
    if id_type not in valid_id_types:
        error_string = f"id_type must be one of {valid_id_types}"
        log.error(error_string)
        raise HTTPException(status_code=404, detail=error_string)

    try:
        return await aggregate(id, id_type)
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
