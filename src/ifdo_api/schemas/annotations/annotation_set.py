from typing import ClassVar
from ifdo_api.schemas.annotations.annotation import AnnotationSchema
from ifdo_api.schemas.annotations.annotation import AnnotatorSchema
from ifdo_api.schemas.annotations.label import LabelSchema
from ifdo_api.schemas.common_fields import CommonFieldsAllSchema
from ifdo_api.schemas.image_set import ImageSetSchema


class AnnotationSetSchema(CommonFieldsAllSchema):
    """Schema for a image_set model, representing a collection of images and their metadata."""

    # handle: HttpUrl

    abstract: str | None = None

    annotations_labels: list[LabelSchema] | None = None
    annotations_creators: list[AnnotatorSchema] | None = None

    version: float | None = None

    image_sets: list[ImageSetSchema] | None = None

    annotations: list[AnnotationSchema] | None = None

    labels: list[LabelSchema] | None = None

    model_config: ClassVar[dict] = {
        "extra": "ignore",  # ignore extra fields
        "from_attributes": True,  # to load from ORM objects
        "exclude_none": True,  # hide fields with value None when serializing
    }
