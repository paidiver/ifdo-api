from fastapi import APIRouter
from ifdo_api.api.generic_router import generate_crud_router
from ifdo_api.crud.annotation import label_crud
from ifdo_api.schemas.annotation import LabelSchema

router: APIRouter = generate_crud_router(
    model_crud=label_crud,
    schema=LabelSchema,
    schema_create=LabelSchema,
)
