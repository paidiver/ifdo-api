from typing import ClassVar
from uuid import UUID
from uuid import uuid4
from pydantic import Field
from ifdo_api.schemas.annotation import AnnotatorSchema
from ifdo_api.schemas.annotation import ImageAnnotationSchema
from ifdo_api.schemas.annotation import LabelSchema
from ifdo_api.schemas.common_fields import CommonFieldsSchema


class ImageSchema(CommonFieldsSchema):
    """Schema for an image, representing its metadata and associated information."""

    uuid: UUID = Field(default_factory=uuid4, description="Unique UUID for the image")

    annotations_labels: list[LabelSchema] = Field(default_factory=list)
    annotations_creators: list[AnnotatorSchema] = Field(default_factory=list)
    annotations: list[ImageAnnotationSchema] = Field(default_factory=list)

    model_config: ClassVar[dict] = {
        "extra": "ignore",
    }


ImageSchema.model_rebuild()
