# ifdo_api/api/v1/fields/image_flatport_parameter.py
from fastapi import APIRouter
from ifdo_api.api.generic_router import generate_crud_router
from ifdo_api.crud.fields import image_flatport_parameter_crud
from ifdo_api.schemas.fields import ImageFlatportParameterSchema

router: APIRouter = generate_crud_router(
    model_crud=image_flatport_parameter_crud,
    schema=ImageFlatportParameterSchema,
    schema_create=ImageFlatportParameterSchema,
)
