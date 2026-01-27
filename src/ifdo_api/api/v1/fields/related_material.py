# ifdo_api/api/v1/fields/related_material.py
from fastapi import APIRouter
from ifdo_api.api.generic_router import generate_crud_router
from ifdo_api.crud.fields import related_material_crud
from ifdo_api.schemas.fields import RelatedMaterialSchema

router: APIRouter = generate_crud_router(
    model_crud=related_material_crud,
    schema=RelatedMaterialSchema,
    schema_create=RelatedMaterialSchema,
)
