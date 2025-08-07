from fastapi import APIRouter
from ifdo_api.api.generic_router import generate_crud_router
from ifdo_api.crud.provenance import provenance_activity_crud
from ifdo_api.schemas.provenance import ProvenanceActivitySchema

router: APIRouter = generate_crud_router(
    model_crud=provenance_activity_crud,
    schema=ProvenanceActivitySchema,
    schema_create=ProvenanceActivitySchema,
)
