"""This module implements the CRUD for the Annotations model."""

from ifdo_api.crud.base import CRUDBase
from ifdo_api.models.annotations.annotation import Annotation
from ifdo_api.models.annotations.annotation import AnnotationLabel
from ifdo_api.models.annotations.annotation import Annotator


class CRUDAnnotation(CRUDBase[Annotation]):
    """CRUD object with default methods to Create, Read, Update, Delete (CRUD).

    Args:
        CRUDBase (ModelType): Base class for CRUD operations.
    """


class CRUDAnnotationLabel(CRUDBase[AnnotationLabel]):
    """CRUD object with default methods to Create, Read, Update, Delete (CRUD).

    Args:
        CRUDBase (ModelType): Base class for CRUD operations.
    """


class CRUDAnnotator(CRUDBase[Annotator]):
    """CRUD object with default methods to Create, Read, Update, Delete (CRUD).

    Args:
        CRUDBase (ModelType): Base class for CRUD operations.
    """


annotation_crud = CRUDAnnotation(Annotation)
annotation_label_crud = CRUDAnnotationLabel(AnnotationLabel)
annotator_crud = CRUDAnnotator(Annotator)
