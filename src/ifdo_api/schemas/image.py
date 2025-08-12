from typing import ClassVar
from uuid import UUID
from pydantic import BaseModel
from ifdo_api.schemas.common_fields import CommonFieldsSchema


class ImageSchema(CommonFieldsSchema):
    """Schema for an image, representing its metadata and associated information."""

    dataset_id: UUID | None = None

    # annotations_labels: list[LabelSchema] = Field(default_factory=list)
    # annotations_creators: list[AnnotatorSchema] = Field(default_factory=list)
    # annotations: list[ImageAnnotationSchema] = Field(default_factory=list)

    model_config: ClassVar[dict] = {
        "extra": "ignore",  # ignore extra fields
        "from_attributes": True,  # to load from ORM objects
        "exclude_none": True,  # hide fields with value None when serializing
    }


class SimpleImageSchema(BaseModel):
    """Schema for a simplified image representation, primarily used for listing images without full metadata."""

    name: str

    model_config = {"from_attributes": True, "extra": "ignore"}


ImageSchema.model_rebuild()
