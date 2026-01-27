from pydantic import BaseModel
from pydantic import Field
from pydantic import HttpUrl
from pydantic import confloat
from pydantic import conlist


class NamedURISchema(BaseModel):
    """A base schema for objects that have a name and an optional URI."""

    name: str = Field(..., max_length=255)
    uri: HttpUrl | None = None


class ContextSchema(NamedURISchema):
    """Schema for context information."""


class ProjectSchema(NamedURISchema):
    """Schema for project information."""


class EventSchema(NamedURISchema):
    """Schema for event information."""


class PlatformSchema(NamedURISchema):
    """Schema for platform information."""


class SensorSchema(NamedURISchema):
    """Schema for sensor information."""


class PISchema(NamedURISchema):
    """Schema for principal investigator information."""


class CreatorSchema(NamedURISchema):
    """Schema for creator information."""


class LicenseSchema(NamedURISchema):
    """Schema for license information."""


class ImageCameraPoseSchema(BaseModel):
    """Schema for camera pose information."""

    utm_zone: str | None = None
    utm_epsg: str | None = None
    utm_east_north_up_meters: conlist(float, min_length=3, max_length=3) | None = None  # type: ignore[valid-type]
    absolute_orientation_utm_matrix: conlist(float, min_length=9, max_length=9) | None = None  # type: ignore[valid-type]


class ImageCameraHousingViewportSchema(BaseModel):
    """Schema for camera housing viewport parameters."""

    viewport_type: str | None = None
    optical_density: confloat(ge=0.0, le=1.0) | None = None  # type: ignore[valid-type]
    thickness_millimeters: confloat(gt=0.0) | None = None  # type: ignore[valid-type]
    extra_description: str | None = None


class ImageFlatportParameterSchema(BaseModel):
    """Schema for flat port parameters."""

    lens_port_distance_millimeters: float | None = None
    interface_normal_direction: conlist(float, min_length=3, max_length=3) | None = None  # type: ignore[valid-type]
    extra_description: str | None = None


class ImageDomeportParameterSchema(BaseModel):
    """Schema for dome port parameters."""

    outer_radius_millimeters: float | None = None
    decentering_offset_xyz_millimeters: conlist(float, min_length=3, max_length=3) | None = None  # type: ignore[valid-type]
    extra_description: str | None = None


class ImageCameraCalibrationModelSchema(BaseModel):
    """Schema for camera calibration model parameters."""

    calibration_model_type: str | None = None
    focal_length_xy_pixel: conlist(float, min_length=2, max_length=2) | None = None  # type: ignore[valid-type]
    principal_point_xy_pixel: conlist(float, min_length=2, max_length=2) | None = None  # type: ignore[valid-type]
    distortion_coefficients: list[float] | None = None
    approximate_field_of_view_water_xy_degree: list[float] | None = None
    extra_description: str | None = None


class ImagePhotometricCalibrationSchema(BaseModel):
    """Schema for photometric calibration parameters."""

    sequence_white_balancing: str | None = None
    exposure_factor_rgb: conlist(float, min_length=3, max_length=3) | None = None  # type: ignore[valid-type]
    sequence_illumination_type: str | None = None
    sequence_illumination_description: str | None = None
    illumination_factor_rgb: conlist(float, min_length=3, max_length=3) | None = None  # type: ignore[valid-type]
    water_properties_description: str | None = None


class RelatedMaterialSchema(BaseModel):
    """Schema for related materials in an image set."""

    uri: HttpUrl
    title: str = Field(..., max_length=255)
    relation: str = Field(...)

    def __str__(self) -> str:
        return f"{self.title} ({self.uri})"
