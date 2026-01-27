# ifdo_api/api/v1/fields/creator.py
from fastapi import APIRouter
from ifdo_api.api.generic_router import generate_crud_router
from ifdo_api.crud.fields import creator_crud
from ifdo_api.schemas.fields import CreatorSchema

router: APIRouter = generate_crud_router(
    model_crud=creator_crud,
    schema=CreatorSchema,
    schema_create=CreatorSchema,
)
