"""This module implements the CRUD for the Labels model."""

from ifdo_api.crud.base import CRUDBase
from ifdo_api.models.annotations import Label

# from ifdo_api.models.annotations import LabelSource


class CRUDLabel(CRUDBase[Label]):
    """CRUD object with default methods to Create, Read, Update, Delete (CRUD).

    Args:
        CRUDBase (ModelType): Base class for CRUD operations.
    """


# class CRUDLabelSource(CRUDBase[LabelSource]):
#     """CRUD object with default methods to Create, Read, Update, Delete (CRUD).

#     Args:
#         CRUDBase (ModelType): Base class for CRUD operations.
#     """


label_crud = CRUDLabel(Label)
# label_source_crud = CRUDLabelSource(LabelSource)
