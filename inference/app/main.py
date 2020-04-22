import base64
import logging

from fastapi import FastAPI, HTTPException

from .src.aggregate import (aggregate_lc_names, aggregate_mesh,
                            aggregate_wikidata)

logger = logging.getLogger(__name__)

# initialise API
logger.info("Starting API")
app = FastAPI(
    title="Concepts Enhancer",
    description="One-stop-shop for sanitizing and enhancing concepts with wikidata",
)
logger.info("API started, awaiting requests")


@app.get("/lc-names/{lc_names_id}")
def lc_names_endpoint(lc_names_id: str):
    try:
        response = aggregate_lc_names(lc_names_id)
        logger.info(f"Aggregated concept data for lc_names ID: {lc_names_id}")
    except ValueError as e:
        error_string = str(e)
        logger.error(error_string)
        raise HTTPException(status_code=404, detail=error_string)
    return response


@app.get("/mesh/{mesh_id}")
def mesh_endpoint(mesh_id: str):
    try:
        response = aggregate_mesh(mesh_id)
        logger.info(f"Aggregated concept data for MeSH ID: {mesh_id}")
    except ValueError as e:
        error_string = str(e)
        logger.error(error_string)
        raise HTTPException(status_code=404, detail=error_string)
    return response


@app.get("/wikidata/{wikidata_id}")
def wikidata_endpoint(wikidata_id: str):
    try:
        response = aggregate_wikidata(wikidata_id)
        logger.info(f"Aggregated concept data for wikidata ID: {wikidata_id}")
    except ValueError as e:
        error_string = str(e)
        logger.error(error_string)
        raise HTTPException(status_code=404, detail=error_string)
    return response


@app.get("/healthcheck")
def healthcheck():
    return {"status": "healthy"}
