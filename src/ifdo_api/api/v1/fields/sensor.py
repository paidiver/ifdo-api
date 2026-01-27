# ifdo_api/api/v1/fields/sensor.py
from fastapi import APIRouter
from ifdo_api.api.generic_router import generate_crud_router
from ifdo_api.crud.fields import sensor_crud
from ifdo_api.schemas.fields import SensorSchema

router: APIRouter = generate_crud_router(
    model_crud=sensor_crud,
    schema=SensorSchema,
    schema_create=SensorSchema,
)
