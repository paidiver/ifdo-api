# ifdo_api/api/v1/fields/image_event.py
from fastapi import APIRouter
from ifdo_api.api.generic_router import generate_crud_router
from ifdo_api.crud.fields import event_crud
from ifdo_api.schemas.fields import EventSchema

router: APIRouter = generate_crud_router(
    model_crud=event_crud,
    schema=EventSchema,
    schema_create=EventSchema,
)
