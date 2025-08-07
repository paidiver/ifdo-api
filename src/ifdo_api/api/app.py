"""FastAPI module that represent the root of the API."""

import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis.asyncio import Redis
from starlette.responses import RedirectResponse
from tipg.collections import register_collection_catalog
from tipg.database import close_db_connection
from tipg.database import connect_to_db
from tipg.errors import DEFAULT_STATUS_CODES
from tipg.errors import add_exception_handlers
from tipg.factory import OGCFeaturesFactory
from tipg.factory import OGCTilesFactory
from tipg.settings import PostgresSettings
from ifdo_api.api.exceptions import AppException
from ifdo_api.api.v1 import dataset
from ifdo_api.api.v1 import image
from ifdo_api.api.v1.annotation import annotation
from ifdo_api.api.v1.annotation import annotation_label
from ifdo_api.api.v1.annotation import annotator
from ifdo_api.api.v1.annotation import label
from ifdo_api.api.v1.fields import image_camera_calibration_model
from ifdo_api.api.v1.fields import image_camera_housing_viewport
from ifdo_api.api.v1.fields import image_camera_pose
from ifdo_api.api.v1.fields import image_context
from ifdo_api.api.v1.fields import image_creator
from ifdo_api.api.v1.fields import image_domeport_parameter
from ifdo_api.api.v1.fields import image_event
from ifdo_api.api.v1.fields import image_flatport_parameter
from ifdo_api.api.v1.fields import image_license
from ifdo_api.api.v1.fields import image_photometric_calibration
from ifdo_api.api.v1.fields import image_pi
from ifdo_api.api.v1.fields import image_platform
from ifdo_api.api.v1.fields import image_project
from ifdo_api.api.v1.fields import image_sensor
from ifdo_api.api.v1.fields import image_set_related_material

# from ifdo_api.api.v1.provenance import provenance_activity
# from ifdo_api.api.v1.provenance import provenance_agent
# from ifdo_api.api.v1.provenance import provenance_entity
from ifdo_api.db.db import get_db_url


@asynccontextmanager
async def lifespan(application: FastAPI) -> asynccontextmanager:
    """Lifespan event handler to initialize Redis cache.

    Args:
        application (FastAPI): The FastAPI application instance.

    Yields:
        None: This function does not return anything, it initializes the Redis cache.
    """
    await connect_to_db(
        application,
        settings=PostgresSettings(database_url=get_db_url(psycopg=False)),
        schemas=["public"],
    )
    await register_collection_catalog(app)

    redis_host = os.getenv("REDIS_HOST", "localhost")
    redis_port = os.getenv("REDIS_PORT", "6379")
    redis = Redis.from_url(f"redis://{redis_host}:{redis_port}")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield
    await redis.close()
    await close_db_connection(application)


app = FastAPI(lifespan=lifespan, title="Paidiver ST3 PG API", version="0.1.0", openapi_url="/openapi.json", docs_url="/docs")


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["GET", "POST", "HEAD", "OPTIONS", "PUT", "DELETE"],
    allow_headers=["Access-Control-Allow-Headers", "Content-Type", "Authorization", "Access-Control-Allow-Origin"],
    allow_credentials=True,
)


@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    """Handle application exceptions.

    Args:
        request (Request): The incoming request.
        exc (AppException): The application exception to handle.

    Returns:
        JSONResponse: A JSON response with the error details.
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail, "type": exc.__class__.__name__, "path": str(request.url)},
    )


@app.get("/", include_in_schema=False)
def main() -> RedirectResponse:
    """Redirect to docs.

    Returns:
        RedirectResponse: RedirectResponse to the documentation
    """
    return RedirectResponse(url="/docs")


@app.get(
    "/healthz",
    description="Health Check.",
    summary="Health Check.",
    operation_id="healthCheck",
    tags=["Health Check"],
)
def ping() -> dict:
    """Health check."""
    return {"ping": "pong!"}


#######################
# V1
#######################

app.include_router(image.router, prefix="/v1/images", tags=["Image"])
app.include_router(dataset.router, prefix="/v1/datasets", tags=["Dataset"])

app.include_router(image_context.router, prefix="/v1/fields/image_contexts", tags=["Fields"])
app.include_router(image_project.router, prefix="/v1/fields/image_projects", tags=["Fields"])
app.include_router(image_event.router, prefix="/v1/fields/image_events", tags=["Fields"])
app.include_router(image_platform.router, prefix="/v1/fields/image_platforms", tags=["Fields"])
app.include_router(image_sensor.router, prefix="/v1/fields/image_sensors", tags=["Fields"])
app.include_router(image_pi.router, prefix="/v1/fields/image_pis", tags=["Fields"])
app.include_router(image_creator.router, prefix="/v1/fields/image_creators", tags=["Fields"])
app.include_router(image_license.router, prefix="/v1/fields/image_licenses", tags=["Fields"])
app.include_router(image_camera_pose.router, prefix="/v1/fields/image_camera_poses", tags=["Fields"])
app.include_router(image_camera_housing_viewport.router, prefix="/v1/fields/image_camera_housing_viewports", tags=["Fields"])
app.include_router(image_flatport_parameter.router, prefix="/v1/fields/image_flatport_parameters", tags=["Fields"])
app.include_router(image_domeport_parameter.router, prefix="/v1/fields/image_domeport_parameters", tags=["Fields"])
app.include_router(image_camera_calibration_model.router, prefix="/v1/fields/image_camera_calibration_models", tags=["Fields"])
app.include_router(image_photometric_calibration.router, prefix="/v1/fields/image_photometric_calibrations", tags=["Fields"])
app.include_router(image_set_related_material.router, prefix="/v1/fields/image_set_related_materials", tags=["Fields"])


app.include_router(annotation_label.router, prefix="/v1/annotations/annotation_labels", tags=["Annotation"])
app.include_router(annotation.router, prefix="/v1/annotations/annotations", tags=["Annotation"])
app.include_router(annotator.router, prefix="/v1/annotations/annotators", tags=["Annotation"])
app.include_router(label.router, prefix="/v1/annotations/labels", tags=["Annotation"])


# app.include_router(provenance_activity.router, prefix="/v1/provenances/activities", tags=["Provenance"])
# app.include_router(provenance_agent.router, prefix="/v1/provenances/agents", tags=["Provenance"])
# app.include_router(provenance_entity.router, prefix="/v1/provenances/entities", tags=["Provenance"])


############## ADD Tipg endpoints here ##############
endpoints_features = OGCFeaturesFactory(with_common=True)
endpoints_tiles = OGCTilesFactory(with_common=True)

app.include_router(endpoints_features.router, prefix="/v1/ogc-features", tags=["OGC Features"])
app.include_router(endpoints_tiles.router, prefix="/v1/ogc-tiles", tags=["OGC Tiles"])


add_exception_handlers(app, DEFAULT_STATUS_CODES)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
