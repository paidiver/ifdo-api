from fastapi import APIRouter
from ifdo_api.api.generic_router import generate_crud_router
from ifdo_api.crud.provenance import provenance_agent_crud
from ifdo_api.schemas.provenance.provenance import ProvenanceAgentSchema

router: APIRouter = generate_crud_router(
    model_crud=provenance_agent_crud,
    schema=ProvenanceAgentSchema,
    schema_create=ProvenanceAgentSchema,
)
