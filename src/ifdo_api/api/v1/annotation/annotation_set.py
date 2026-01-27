from fastapi import APIRouter
from ifdo_api.api.generic_router import generate_crud_router
from ifdo_api.crud.annotations.annotation_set import annotation_set_crud
from ifdo_api.schemas.annotations.annotation_set import AnnotationSetSchema

router: APIRouter = generate_crud_router(
    model_crud=annotation_set_crud,
    schema=AnnotationSetSchema,
    schema_create=AnnotationSetSchema,
)
