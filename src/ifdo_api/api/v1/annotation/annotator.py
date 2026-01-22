from fastapi import APIRouter
from ifdo_api.api.generic_router import generate_crud_router
from ifdo_api.crud.annotations.annotation import annotator_crud
from ifdo_api.schemas.annotations.annotation import AnnotatorSchema

router: APIRouter = generate_crud_router(
    model_crud=annotator_crud,
    schema=AnnotatorSchema,
    schema_create=AnnotatorSchema,
)
