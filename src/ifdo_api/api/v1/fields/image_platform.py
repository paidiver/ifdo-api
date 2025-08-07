# ifdo_api/api/v1/fields/image_platform.py
from fastapi import APIRouter
from ifdo_api.api.generic_router import generate_crud_router
from ifdo_api.crud.fields import image_platform_crud
from ifdo_api.schemas.fields import ImagePlatformSchema

router: APIRouter = generate_crud_router(
    model_crud=image_platform_crud,
    schema=ImagePlatformSchema,
    schema_create=ImagePlatformSchema,
)
