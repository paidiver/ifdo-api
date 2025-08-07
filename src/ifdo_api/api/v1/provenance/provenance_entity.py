from fastapi import APIRouter
from ifdo_api.api.generic_router import generate_crud_router
from ifdo_api.crud.provenance import provenance_entity_crud
from ifdo_api.schemas.provenance import ProvenanceEntitySchema

router: APIRouter = generate_crud_router(
    model_crud=provenance_entity_crud,
    schema=ProvenanceEntitySchema,
    schema_create=ProvenanceEntitySchema,
)
