# ifdo_api/api/v1/fields/pi.py
from fastapi import APIRouter
from ifdo_api.api.generic_router import generate_crud_router
from ifdo_api.crud.fields import pi_crud
from ifdo_api.schemas.fields import PISchema

router: APIRouter = generate_crud_router(
    model_crud=pi_crud,
    schema=PISchema,
    schema_create=PISchema,
)
