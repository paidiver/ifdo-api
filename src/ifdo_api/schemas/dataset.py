from typing import ClassVar
from uuid import UUID
from uuid import uuid4
from pydantic import BaseModel
from pydantic import Field
from pydantic import HttpUrl
from ifdo_api.schemas.annotation import AnnotatorSchema
from ifdo_api.schemas.annotation import LabelSchema
from ifdo_api.schemas.common_fields import CommonFieldsSchema
from ifdo_api.schemas.fields import ImageSetRelatedMaterialSchema


class LocationSchema(BaseModel):
    """Schema for geographic coordinates, representing latitude and longitude."""

    lat: float = Field(..., ge=-90, le=90)
    lon: float = Field(..., ge=-180, le=180)


# Main Pydantic model
class DatasetSchema(CommonFieldsSchema):
    """Schema for a dataset model, representing a collection of images and their metadata."""

    uuid: UUID = Field(default_factory=uuid4)
    handle: HttpUrl
    local_path: str = Field(default="../raw", max_length=500)

    min_latitude_degrees: float = Field(..., ge=-90, le=90)
    max_latitude_degrees: float = Field(..., ge=-90, le=90)
    min_longitude_degrees: float = Field(..., ge=-180, le=180)
    max_longitude_degrees: float = Field(..., ge=-180, le=180)

    related_materials: list[ImageSetRelatedMaterialSchema] = Field(default_factory=list)

    annotations_labels: list[LabelSchema] = Field(default_factory=list)
    annotations_creators: list[AnnotatorSchema] = Field(default_factory=list)

    # provenance_agents: list[str] = Field(default_factory=list)
    # provenance_entities: list[str] = Field(default_factory=list)
    # provenance_activities: list[str] = Field(default_factory=list)

    model_config: ClassVar[dict] = {
        "extra": "ignore",
    }


DatasetSchema.model_rebuild()
