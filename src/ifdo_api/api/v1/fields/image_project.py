# ifdo_api/api/v1/fields/image_project.py
from fastapi import APIRouter
from ifdo_api.api.generic_router import generate_crud_router
from ifdo_api.crud.fields import image_project_crud
from ifdo_api.schemas.fields import ImageProjectSchema

router: APIRouter = generate_crud_router(
    model_crud=image_project_crud,
    schema=ImageProjectSchema,
    schema_create=ImageProjectSchema,
)
