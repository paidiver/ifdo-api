# ifdo_api/api/v1/fields/image_sensor.py
from fastapi import APIRouter
from ifdo_api.api.generic_router import generate_crud_router
from ifdo_api.crud.fields import image_sensor_crud
from ifdo_api.schemas.fields import ImageSensorSchema

router: APIRouter = generate_crud_router(
    model_crud=image_sensor_crud,
    schema=ImageSensorSchema,
    schema_create=ImageSensorSchema,
)
