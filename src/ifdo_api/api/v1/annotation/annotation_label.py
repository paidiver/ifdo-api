from fastapi import APIRouter
from ifdo_api.api.generic_router import generate_crud_router
from ifdo_api.crud.annotation import annotation_label_crud
from ifdo_api.schemas.annotation import AnnotationLabelSchema

router: APIRouter = generate_crud_router(
    model_crud=annotation_label_crud,
    schema=AnnotationLabelSchema,
    schema_create=AnnotationLabelSchema,
)
