"""This module implements the CRUD for the ProvenanceActivity model."""

from ifdo_api.crud.base import CRUDBase
from ifdo_api.models.provenance import ProvenanceActivity
from ifdo_api.models.provenance import ProvenanceAgent
from ifdo_api.models.provenance import ProvenanceEntity


class CRUDProvenanceActivity(CRUDBase[ProvenanceActivity]):
    """CRUD object with default methods to Create, Read, Update, Delete (CRUD).

    Args:
        CRUDBase (ModelType): Base class for CRUD operations.
    """


class CRUDProvenanceAgent(CRUDBase[ProvenanceAgent]):
    """CRUD object with default methods to Create, Read, Update, Delete (CRUD).

    Args:
        CRUDBase (ModelType): Base class for CRUD operations.
    """


class CRUDProvenanceEntity(CRUDBase[ProvenanceEntity]):
    """CRUD object with default methods to Create, Read, Update, Delete (CRUD).

    Args:
        CRUDBase (ModelType): Base class for CRUD operations.
    """


provenance_activity_crud = CRUDProvenanceActivity(ProvenanceActivity)
provenance_agent_crud = CRUDProvenanceAgent(ProvenanceAgent)
provenance_entity_crud = CRUDProvenanceEntity(ProvenanceEntity)
