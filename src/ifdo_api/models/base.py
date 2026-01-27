import enum
from datetime import datetime
from datetime import timezone
from uuid import uuid4
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class DefaultColumns:
    """Mixin class to add created_at and updated_at timestamps to a model."""

    # id = Column(
    #     Integer,
    #     primary_key=True,
    #     autoincrement=True,
    # )
    id = Column(
        UUID,
        primary_key=True,
        nullable=False,
        unique=True,
        default=uuid4,
    )
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)


class CaseInsensitiveEnum(str, enum.Enum):
    """Base Enum that allows case-insensitive matching."""

    @classmethod
    def _missing_(cls, value: str) -> "CaseInsensitiveEnum | None":
        if isinstance(value, str):
            for member in cls:
                if member.value.lower() == value.lower():
                    return member
        return None


class ShapeEnum(str, enum.Enum):
    """Enumeration of possible annotation shapes."""

    single_pixel = "single-pixel"
    polyline = "polyline"
    polygon = "polygon"
    circle = "circle"
    rectangle = "rectangle"
    ellipse = "ellipse"
    whole_image = "whole-image"


class AcquisitionEnum(CaseInsensitiveEnum):
    """Enumeration for acquisition types in the system."""

    photo = "photo"
    video = "video"
    slide = "slide"


class NavigationEnum(CaseInsensitiveEnum):
    """Enumeration for navigation types in the system."""

    satellite = "satellite"
    beacon = "beacon"
    transponder = "transponder"
    reconstructed = "reconstructed"


class ScaleReferenceEnum(CaseInsensitiveEnum):
    """Enumeration for scale references in the system."""

    camera_3d = "3D camera"
    camera_calibrated = "calibrated camera"
    laser_marker = "laser marker"
    optical_flow = "optical flow"


class IlluminationEnum(CaseInsensitiveEnum):
    """Enumeration for illumination types in the system."""

    sunlight = "sunlight"
    artificial_light = "artificial light"
    mixed_light = "mixed light"


class PixelMagnitudeEnum(CaseInsensitiveEnum):
    """Enumeration for pixel magnitude types in the system."""

    km = "km"
    hm = "hm"
    dam = "dam"
    m = "m"
    cm = "cm"
    mm = "mm"
    um = "µm"


class MarineZoneEnum(CaseInsensitiveEnum):
    """Enumeration for marine zones in the system."""

    seafloor = "seafloor"
    water_column = "water column"
    sea_surface = "sea surface"
    atmosphere = "atmosphere"
    laboratory = "laboratory"


class SpectralResEnum(CaseInsensitiveEnum):
    """Enumeration for spectral resolution types in the system."""

    grayscale = "grayscale"
    rgb = "rgb"
    multi_spectral = "multi-spectral"
    hyper_spectral = "hyper-spectral"


class CaptureModeEnum(CaseInsensitiveEnum):
    """Enumeration for capture modes in the system."""

    timer = "timer"
    manual = "manual"
    mixed = "mixed"


class FaunaAttractionEnum(CaseInsensitiveEnum):
    """Enumeration for fauna attraction methods in the system."""

    none = "none"
    baited = "baited"
    light = "light"


class DeploymentEnum(CaseInsensitiveEnum):
    """Enumeration for deployment types in the system."""

    mapping = "mapping"
    stationary = "stationary"
    survey = "survey"
    exploration = "exploration"
    experiment = "experiment"
    sampling = "sampling"


class QualityEnum(CaseInsensitiveEnum):
    """Enumeration for quality types in the system."""

    raw = "raw"
    processed = "processed"
    product = "product"
