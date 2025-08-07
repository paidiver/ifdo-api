# ifdo_api/api/v1/fields/image_event.py
from fastapi import APIRouter
from ifdo_api.api.generic_router import generate_crud_router
from ifdo_api.crud.fields import image_event_crud
from ifdo_api.schemas.fields import ImageEventSchema

router: APIRouter = generate_crud_router(
    model_crud=image_event_crud,
    schema=ImageEventSchema,
    schema_create=ImageEventSchema,
)
