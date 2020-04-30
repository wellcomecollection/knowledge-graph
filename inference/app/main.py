import base64
import logging

from fastapi import FastAPI, HTTPException

from .src.aggregate import aggregate

logger = logging.getLogger(__name__)

# initialise API
logger.info("Starting API")
app = FastAPI(
    title="Concepts Enhancer",
    description="One-stop-shop for sanitizing and enhancing concepts with wikidata",
)
logger.info("API started, awaiting requests")


@app.get("/lc-names/{query_id}")
def lc_names_endpoint(query_id: str):
    try:
        response = aggregate(query_id=query_id, id_type="lc_names")
        logger.info(f"Aggregated concept data for lc_names ID: {query_id}")
    except ValueError as e:
        error_string = str(e)
        logger.error(error_string)
        raise HTTPException(status_code=404, detail=error_string)
    return response


@app.get("/lc-subjects/{query_id}")
def lc_subjects_endpoint(query_id: str):
    try:
        response = aggregate(query_id=query_id, id_type="lc_subjects")
        logger.info(f"Aggregated concept data for lc_subjects ID: {query_id}")
    except ValueError as e:
        error_string = str(e)
        logger.error(error_string)
        raise HTTPException(status_code=404, detail=error_string)
    return response


@app.get("/mesh/{query_id}")
def mesh_endpoint(query_id: str):
    try:
        response = aggregate(query_id=query_id, id_type="mesh")
        logger.info(f"Aggregated concept data for MeSH ID: {query_id}")
    except ValueError as e:
        error_string = str(e)
        logger.error(error_string)
        raise HTTPException(status_code=404, detail=error_string)
    return response


@app.get("/wikidata/{query_id}")
def wikidata_endpoint(query_id: str):
    try:
        response = aggregate(query_id=query_id, id_type="wikidata")
        logger.info(f"Aggregated concept data for wikidata ID: {query_id}")
    except ValueError as e:
        error_string = str(e)
        logger.error(error_string)
        raise HTTPException(status_code=404, detail=error_string)
    return response


@app.get("/healthcheck")
def healthcheck():
    return {"status": "healthy"}
