from fastapi import APIRouter
from ifdo_api.api.generic_router import generate_crud_router
from ifdo_api.crud.annotations.label import label_source_crud
from ifdo_api.schemas.annotations.label import LabelSourceSchema

router: APIRouter = generate_crud_router(
    model_crud=label_source_crud,
    schema=LabelSourceSchema,
    schema_create=LabelSourceSchema,
)
