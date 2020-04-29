import base64
import logging
import time

from fastapi import FastAPI, HTTPException

from .src.aggregate import aggregate
from .src.http import (close_persistent_client_session,
                       start_persistent_client_session)
from .src.wikidata import search_wikidata

logger = logging.getLogger(__name__)

# initialise API
logger.info("Starting API")
app = FastAPI(
    title="Concepts Enhancer",
    description="One-stop-shop for sanitizing and enhancing concepts with wikidata",
)
logger.info("API started, awaiting requests")


@app.get("/lc-names/{query_id}")
async def lc_names_endpoint(query_id: str):
    try:
        start_time = time.time()
        response = await aggregate(
            query_id=query_id,
            id_type="lc_names",
            confidence="exact"
        )
        logger.info(
            f"Aggregated concept data for lc_names ID: {query_id}"
            f", which took took {round(time.time() - start_time, 2)}s"
        )
    except ValueError as e:
        error_string = str(e)
        logger.error(error_string)
        raise HTTPException(status_code=404, detail=error_string)
    return response


@app.get("/lc-subjects/{query_id}")
async def lc_subjects_endpoint(query_id: str):
    try:
        start_time = time.time()
        response = await aggregate(
            query_id=query_id,
            id_type="lc_subjects",
            confidence="exact"
        )
        logger.info(
            f"Aggregated concept data for lc_subjects ID: {query_id}"
            f", which took took {round(time.time() - start_time, 2)}s"
        )
    except ValueError as e:
        error_string = str(e)
        logger.error(error_string)
        raise HTTPException(status_code=404, detail=error_string)
    return response


@app.get("/mesh/{query_id}")
async def mesh_endpoint(query_id: str):
    try:
        start_time = time.time()
        response = await aggregate(
            query_id=query_id,
            id_type="mesh",
            confidence="exact"
        )
        logger.info(
            f"Aggregated concept data for MeSH ID: {query_id}"
            f", which took took {round(time.time() - start_time, 2)}s"
        )
    except ValueError as e:
        error_string = str(e)
        logger.error(error_string)
        raise HTTPException(status_code=404, detail=error_string)
    return response


@app.get("/wikidata/{query_id}")
async def wikidata_endpoint(query_id: str):
    try:
        start_time = time.time()
        response = await aggregate(
            query_id=query_id,
            id_type="wikidata",
            confidence="exact"
        )
        logger.info(
            f"Aggregated concept data for wikidata ID: {query_id}"
            f", which took took {round(time.time() - start_time, 2)}s"
        )
    except ValueError as e:
        error_string = str(e)
        logger.error(error_string)
        raise HTTPException(status_code=404, detail=error_string)
    return response


@app.get("/search/{query}")
async def search_endpoint(query: str):
    try:
        start_time = time.time()
        wikidata_id = await search_wikidata(query)
        response = await aggregate(
            query_id=wikidata_id,
            id_type="wikidata",
            confidence="inferred"
        )
        logger.info(
            f"Aggregated concept data for wikidata ID: {wikidata_id}"
            f", which took took {round(time.time() - start_time, 2)}s"
        )
    except ValueError as e:
        error_string = str(e)
        logger.error(error_string)
        raise HTTPException(status_code=404, detail=error_string)
    return response


@app.get("/healthcheck")
def healthcheck():
    return {"status": "healthy"}


@app.on_event("startup")
def on_startup():
    start_persistent_client_session()


@app.on_event("shutdown")
async def on_shutdown():
    await close_persistent_client_session()
