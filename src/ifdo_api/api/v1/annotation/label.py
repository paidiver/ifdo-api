from fastapi import APIRouter
from ifdo_api.api.generic_router import generate_crud_router
from ifdo_api.crud.annotations.label import label_crud
from ifdo_api.schemas.annotations.label import LabelSchema

router: APIRouter = generate_crud_router(
    model_crud=label_crud,
    schema=LabelSchema,
    schema_create=LabelSchema,
)
