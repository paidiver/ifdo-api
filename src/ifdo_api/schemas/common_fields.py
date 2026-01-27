from datetime import datetime
from typing import Any
from typing import ClassVar
from uuid import UUID
from pydantic import BaseModel
from pydantic import Field
from pydantic import HttpUrl
from pydantic import conint
from pydantic import conlist
from ifdo_api.schemas.fields import ContextSchema
from ifdo_api.schemas.fields import CreatorSchema
from ifdo_api.schemas.fields import EventSchema
from ifdo_api.schemas.fields import ImageCameraCalibrationModelSchema
from ifdo_api.schemas.fields import ImageCameraHousingViewportSchema
from ifdo_api.schemas.fields import ImageCameraPoseSchema
from ifdo_api.schemas.fields import ImageDomeportParameterSchema
from ifdo_api.schemas.fields import ImageFlatportParameterSchema
from ifdo_api.schemas.fields import ImagePhotometricCalibrationSchema
from ifdo_api.schemas.fields import LicenseSchema
from ifdo_api.schemas.fields import PISchema
from ifdo_api.schemas.fields import PlatformSchema
from ifdo_api.schemas.fields import ProjectSchema
from ifdo_api.schemas.fields import SensorSchema


class CommonFieldsImageImageSetSchema(BaseModel):
    """Schema for common fields shared across various models, representing metadata and associated information."""

    sha256_hash: str | None = None
    date_time: datetime | None = None
    latitude: float | None = None
    longitude: float | None = None

    # sha256_hash: str = Field(..., max_length=64)
    # date_time: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    # latitude: float = Field(..., ge=-90, le=90)
    # longitude: float = Field(..., ge=-180, le=180)

    # location: Point = Field(..., description="WGS84 geographic center location")
    altitude_meters: float | None = None
    coordinate_uncertainty_m: float | None = None
    event: EventSchema | None = None

    entropy: float | None = None
    particle_count: int | None = None

    # entropy: float | None = Field(default=None, ge=0.0, le=1.0)
    # particle_count: int | None = Field(default=None, ge=0)
    average_color: conlist(conint(ge=0, le=255), min_length=3, max_length=3) | None = None  # type: ignore[valid-type]
    mpeg7_color_layout: list[float] | None = None
    mpeg7_color_statistic: list[float] | None = None
    mpeg7_color_structure: list[float] | None = None
    mpeg7_dominant_color: list[float] | None = None
    mpeg7_edge_histogram: list[float] | None = None
    mpeg7_homogeneous_texture: list[float] | None = None
    mpeg7_scalable_color: list[float] | None = None

    acquisition: str | None = None
    quality: str | None = None
    deployment: str | None = None
    navigation: str | None = None
    scale_reference: str | None = None
    illumination: str | None = None
    pixel_magnitude: str | None = None
    marine_zone: str | None = None
    spectral_resolution: str | None = None
    capture_mode: str | None = None
    fauna_attraction: str | None = None

    area_square_meters: float | None = None
    # area_square_meters: float | None = Field(default=None, gt=0.0, description="Area in square meters, must be greater than 0")
    meters_above_ground: float | None = None
    acquisition_settings: dict[str, Any] | None = None

    camera_yaw_degrees: float | None = None
    camera_pitch_degrees: float | None = None
    camera_roll_degrees: float | None = None

    overlap_fraction: float | None = None
    # overlap_fraction: float | None = Field(default=None, ge=0.0, le=1.0)

    camera_pose: ImageCameraPoseSchema | None = None
    camera_housing_viewport: ImageCameraHousingViewportSchema | None = None
    flatport_parameter: ImageFlatportParameterSchema | None = None
    domeport_parameter: ImageDomeportParameterSchema | None = None
    camera_calibration_model: ImageCameraCalibrationModelSchema | None = None
    photometric_calibration: ImagePhotometricCalibrationSchema | None = None

    objective: str | None = None
    target_environment: str | None = None
    target_timescale: str | None = None
    spatial_constraints: str | None = None
    temporal_constraints: str | None = None
    time_synchronisation: str | None = None
    item_identification_scheme: str | None = None
    curation_protocol: str | None = None
    visual_constraints: str | None = None

    model_config: ClassVar[dict] = {
        "from_attributes": True,  # to load from ORM objects
        "exclude_none": True,  # hide fields with value None when serializing
    }


class CommonFieldsAllSchema(BaseModel):
    """Schema for common fields shared across various models, representing metadata and associated information."""

    id: UUID | None = None
    # Field(default_factory=uuid4, description="Unique UUID for the image/image_set")

    name: str = Field(..., max_length=255)
    handle: HttpUrl | None = None

    copyright: str | None = None
    abstract: str | None = None

    context: ContextSchema | None = None
    project: ProjectSchema | None = None
    platform: PlatformSchema | None = None
    sensor: SensorSchema | None = None
    pi: PISchema | None = None
    license: LicenseSchema | None = None

    creators: list[CreatorSchema] = Field(default_factory=list)

    model_config: ClassVar[dict] = {
        "from_attributes": True,  # to load from ORM objects
        "exclude_none": True,  # hide fields with value None when serializing
    }
