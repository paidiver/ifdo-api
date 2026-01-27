# ifdo_api/api/v1/fields/license_info.py
# This file is renamed as license_info.py to avoid conflict with hte built-in license module
from fastapi import APIRouter
from ifdo_api.api.generic_router import generate_crud_router
from ifdo_api.crud.fields import license_crud
from ifdo_api.schemas.fields import LicenseSchema

router: APIRouter = generate_crud_router(
    model_crud=license_crud,
    schema=LicenseSchema,
    schema_create=LicenseSchema,
)
