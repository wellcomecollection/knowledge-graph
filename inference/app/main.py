import base64
import logging

from fastapi import FastAPI, HTTPException

from .src.aggregate import aggregate_lc_names_data, aggregate_mesh_data

logger = logging.getLogger(__name__)

# initialise API
logger.info("Starting API")
app = FastAPI(
    title="Concepts Enhancer",
    description="One stop shop for sanitising and enhancing concepts with wikidata",
)
logger.info("API started, awaiting requests")


@app.get("/lc-names/{lc_names_id}")
def lc_names_endpoint(lc_names_id: str):
    try:
        response = aggregate_lc_names_data(lc_names_id)
    except ValueError as e:
        error_string = str(e)
        logger.error(error_string)
        raise HTTPException(status_code=404, detail=error_string)

    logger.info(f"aggregated concept data for lc_names ID: {lc_names_id}")
    return response


@app.get("/mesh/{mesh_id}")
def mesh_endpoint(mesh_id: str):
    try:
        response = aggregate_mesh_data(mesh_id)
    except ValueError as e:
        error_string = str(e)
        logger.error(error_string)
        raise HTTPException(status_code=404, detail=error_string)

    logger.info(f"aggregated concept data for lc_names ID: {mesh_id}")
    return response


@app.get("/healthcheck")
def healthcheck():
    return {"status": "healthy"}
