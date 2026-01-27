"""This module implements the CRUD for the Annotations model."""

from ifdo_api.crud.base import CRUDBase
from ifdo_api.models.annotations.annotation_set import AnnotationSet


class CRUDAnnotationSet(CRUDBase[AnnotationSet]):
    """CRUD object with default methods to Create, Read, Update, Delete (CRUD).

    Args:
        CRUDBase (ModelType): Base class for CRUD operations.
    """


annotation_set_crud = CRUDAnnotationSet(AnnotationSet)
