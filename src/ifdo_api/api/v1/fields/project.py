# ifdo_api/api/v1/fields/project.py
from fastapi import APIRouter
from ifdo_api.api.generic_router import generate_crud_router
from ifdo_api.crud.fields import project_crud
from ifdo_api.schemas.fields import ProjectSchema

router: APIRouter = generate_crud_router(
    model_crud=project_crud,
    schema=ProjectSchema,
    schema_create=ProjectSchema,
)
