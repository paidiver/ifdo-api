# ifdo_api/api/v1/fields/image_creator.py
from fastapi import APIRouter
from ifdo_api.api.generic_router import generate_crud_router
from ifdo_api.crud.fields import image_creator_crud
from ifdo_api.schemas.fields import ImageCreatorSchema

router: APIRouter = generate_crud_router(
    model_crud=image_creator_crud,
    schema=ImageCreatorSchema,
    schema_create=ImageCreatorSchema,
)
