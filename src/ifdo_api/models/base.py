import enum
from datetime import datetime
from datetime import timezone
from uuid import uuid4
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class DefaultColumns:
    """Mixin class to add created_at and updated_at timestamps to a model."""

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    uuid = Column(
        UUID(as_uuid=True),
        nullable=False,
        unique=True,
        default=uuid4,
    )
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)


class AcquisitionEnum(str, enum.Enum):
    """Enumeration for acquisition types in the system."""

    photo = "photo"
    video = "video"
    slide = "slide"


class NavigationEnum(str, enum.Enum):
    """Enumeration for navigation types in the system."""

    satellite = "satellite"
    beacon = "beacon"
    transponder = "transponder"
    reconstructed = "reconstructed"


class ScaleReferenceEnum(str, enum.Enum):
    """Enumeration for scale references in the system."""

    camera_3d = "3D camera"
    camera_calibrated = "Calibrated camera"
    laser_marker = "Laser marker"
    optical_flow = "Optical flow"


class IlluminationEnum(str, enum.Enum):
    """Enumeration for illumination types in the system."""

    sunlight = "sunlight"
    artificial_light = "artificial light"
    mixed_light = "mixed light"


class PixelMagnitudeEnum(str, enum.Enum):
    """Enumeration for pixel magnitude types in the system."""

    km = "km"
    hm = "hm"
    dam = "dam"
    m = "m"
    cm = "cm"
    mm = "mm"
    um = "µm"


class MarineZoneEnum(str, enum.Enum):
    """Enumeration for marine zones in the system."""

    seafloor = "seafloor"
    water_column = "water column"
    sea_surface = "sea surface"
    atmosphere = "atmosphere"
    laboratory = "laboratory"


class SpectralResEnum(str, enum.Enum):
    """Enumeration for spectral resolution types in the system."""

    grayscale = "grayscale"
    rgb = "rgb"
    multi_spectral = "multi-spectral"
    hyper_spectral = "hyper-spectral"


class CaptureModeEnum(str, enum.Enum):
    """Enumeration for capture modes in the system."""

    timer = "timer"
    manual = "manual"
    mixed = "mixed"


class FaunaAttractionEnum(str, enum.Enum):
    """Enumeration for fauna attraction methods in the system."""

    none = "none"
    baited = "baited"
    light = "light"


class DeploymentEnum(str, enum.Enum):
    """Enumeration for deployment types in the system."""

    mapping = "mapping"
    stationary = "stationary"
    survey = "survey"
    exploration = "exploration"
    experiment = "experiment"
    sampling = "sampling"


class QualityEnum(str, enum.Enum):
    """Enumeration for quality types in the system."""

    raw = "raw"
    processed = "processed"
    product = "product"
