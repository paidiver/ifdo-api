from typing import ClassVar
from pydantic import BaseModel
from pydantic import Field
from ifdo_api.schemas.annotations.annotation import AnnotatorSchema
from ifdo_api.schemas.annotations.label import LabelSchema
from ifdo_api.schemas.common_fields import CommonFieldsAllSchema
from ifdo_api.schemas.common_fields import CommonFieldsImageImageSetSchema
from ifdo_api.schemas.fields import RelatedMaterialSchema
from ifdo_api.schemas.image import ImageSchema
from ifdo_api.schemas.image import SimpleImageSchema


class LocationSchema(BaseModel):
    """Schema for geographic coordinates, representing latitude and longitude."""

    lat: float = Field(..., ge=-90, le=90)
    lon: float = Field(..., ge=-180, le=180)


class ImageSetSchema(CommonFieldsImageImageSetSchema, CommonFieldsAllSchema):
    """Schema for a image_set model, representing a collection of images and their metadata."""

    # handle: HttpUrl

    local_path: str = Field(default="../raw", max_length=500)
    # geom: str = Field(..., max_length=1000)
    # limits: str | None = None

    min_latitude_degrees: float | None = None
    max_latitude_degrees: float | None = None
    min_longitude_degrees: float | None = None
    max_longitude_degrees: float | None = None

    # min_latitude_degrees: float = Field(..., ge=-90, le=90)
    # max_latitude_degrees: float = Field(..., ge=-90, le=90)
    # min_longitude_degrees: float = Field(..., ge=-180, le=180)
    # max_longitude_degrees: float = Field(..., ge=-180, le=180)

    related_materials: list[RelatedMaterialSchema] = Field(default_factory=list)

    annotations_labels: list[LabelSchema] | None = None
    annotations_creators: list[AnnotatorSchema] | None = None

    # provenance_agents: list[str] = Field(default_factory=list)
    # provenance_entities: list[str] = Field(default_factory=list)
    # provenance_activities: list[str] = Field(default_factory=list)

    model_config: ClassVar[dict] = {
        "extra": "ignore",  # ignore extra fields
        "from_attributes": True,  # to load from ORM objects
        "exclude_none": True,  # hide fields with value None when serializing
    }


class ImageSetFullSchema(ImageSetSchema):
    """Schema for a image_set model, representing a collection of images and their metadata with full image information."""

    images: list[ImageSchema] | None = None


class ImageSetSimpleSchema(ImageSetSchema):
    """Schema for a image_set model, representing a collection of images and their metadata with simplified image information."""

    images: list[SimpleImageSchema] | None = None


ImageSetSchema.model_rebuild()
