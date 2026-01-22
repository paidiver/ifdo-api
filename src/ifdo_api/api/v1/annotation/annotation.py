from fastapi import APIRouter
from ifdo_api.api.generic_router import generate_crud_router
from ifdo_api.crud.annotations.annotation import annotation_crud
from ifdo_api.schemas.annotations.annotation import ImageAnnotationSchema

router: APIRouter = generate_crud_router(
    model_crud=annotation_crud,
    schema=ImageAnnotationSchema,
    schema_create=ImageAnnotationSchema,
)
