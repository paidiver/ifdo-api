# ifdo_api/api/v1/fields/image_license.py
from fastapi import APIRouter
from ifdo_api.api.generic_router import generate_crud_router
from ifdo_api.crud.fields import image_license_crud
from ifdo_api.schemas.fields import ImageLicenseSchema

router: APIRouter = generate_crud_router(
    model_crud=image_license_crud,
    schema=ImageLicenseSchema,
    schema_create=ImageLicenseSchema,
)
