# ifdo_api/api/v1/fields/context.py
from fastapi import APIRouter
from ifdo_api.api.generic_router import generate_crud_router
from ifdo_api.crud.fields import context_crud
from ifdo_api.schemas.fields import ContextSchema

router: APIRouter = generate_crud_router(
    model_crud=context_crud,
    schema=ContextSchema,
    schema_create=ContextSchema,
)
