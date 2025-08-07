# ifdo_api/api/v1/fields/image_domeport_parameter.py
from fastapi import APIRouter
from ifdo_api.api.generic_router import generate_crud_router
from ifdo_api.crud.fields import image_domeport_parameter_crud
from ifdo_api.schemas.fields import ImageDomeportParameterSchema

router: APIRouter = generate_crud_router(
    model_crud=image_domeport_parameter_crud,
    schema=ImageDomeportParameterSchema,
    schema_create=ImageDomeportParameterSchema,
)
