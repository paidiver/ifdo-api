# ifdo_api/api/v1/fields/platform.py
from fastapi import APIRouter
from ifdo_api.api.generic_router import generate_crud_router
from ifdo_api.crud.fields import platform_crud
from ifdo_api.schemas.fields import PlatformSchema

router: APIRouter = generate_crud_router(
    model_crud=platform_crud,
    schema=PlatformSchema,
    schema_create=PlatformSchema,
)
