# ifdo_api/api/v1/fields/image_pi.py
from fastapi import APIRouter
from ifdo_api.api.generic_router import generate_crud_router
from ifdo_api.crud.fields import image_pi_crud
from ifdo_api.schemas.fields import ImagePISchema

router: APIRouter = generate_crud_router(
    model_crud=image_pi_crud,
    schema=ImagePISchema,
    schema_create=ImagePISchema,
)
