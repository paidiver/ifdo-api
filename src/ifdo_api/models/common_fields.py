from geoalchemy2 import Geometry
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Enum
from sqlalchemy import Float
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.dialects.postgresql import JSONB
from ifdo_api.models.base import AcquisitionEnum
from ifdo_api.models.base import CaptureModeEnum
from ifdo_api.models.base import DeploymentEnum
from ifdo_api.models.base import FaunaAttractionEnum
from ifdo_api.models.base import IlluminationEnum
from ifdo_api.models.base import MarineZoneEnum
from ifdo_api.models.base import NavigationEnum
from ifdo_api.models.base import PixelMagnitudeEnum
from ifdo_api.models.base import QualityEnum
from ifdo_api.models.base import ScaleReferenceEnum
from ifdo_api.models.base import SpectralResEnum


class CommonFieldsImagesImageSets:
    """Common fields for image_sets and images."""

    sha256_hash = Column(
        String(64),
        nullable=True,
        # nullable=False,
        unique=True,
        info={"help_text": "An SHA256 hash to represent the whole file for integrity verification"},
    )
    date_time = Column(
        DateTime,
        nullable=True,
        # nullable=False,
        info={"help_text": "UTC time of image acquisition (or start time of a video)"},
    )
    geom = Column(
        Geometry(geometry_type="POINT", srid=4326),
        nullable=True,
        # nullable=False,
        info={"help_text": "Geographic location of the center of the image set, in WGS84 coordinates (EPSG:4326)"},
    )
    latitude = Column(
        Float,
        nullable=True,
        # nullable=False,
        info={"help_text": "Latitude of the camera center in degrees, WGS84 coordinates (EPSG:4326)"},
    )
    longitude = Column(
        Float,
        nullable=True,
        # nullable=False,
        info={"help_text": "Longitude of the camera center in degrees, WGS84 coordinates (EPSG:4326)"},
    )
    altitude_meters = Column(
        Float,
        nullable=True,
        # nullable=False,
        info={"help_text": "Z-coordinate of camera center in meters. Positive above sea level, negative below."},
    )
    coordinate_uncertainty_meters = Column(
        Float,
        nullable=True,
        info={"help_text": "The average/static uncertainty of coordinates in this image_set, in meters."},
    )

    entropy = Column(
        Float,
        nullable=True,
        info={"help_text": "Information content of an image / frame according to Shannon entropy."},
    )

    particle_count = Column(Integer, nullable=True, info={"help_text": "Counts of single particles/objects in an image / frame"})

    average_color = Column(
        ARRAY(Float),
        nullable=True,
        info={
            "help_text": (
                "The average colour for each image / frame and the n channels of an image (e.g. 3 for RGB). The values are in the range 0-255."
            )
        },
    )

    mpeg7_color_layout = Column(
        ARRAY(Float),
        nullable=True,
        info={"help_text": "An nD feature vector per image / frame of varying dimensionality according to the chosen descriptor settings."},
    )

    mpeg7_color_statistic = Column(
        ARRAY(Float),
        nullable=True,
        info={"help_text": "An nD feature vector per image / frame of varying dimensionality according to the chosen descriptor settings."},
    )

    mpeg7_color_structure = Column(
        ARRAY(Float),
        nullable=True,
        info={"help_text": "An nD feature vector per image / frame of varying dimensionality according to the chosen descriptor settings."},
    )

    mpeg7_dominant_color = Column(
        ARRAY(Float),
        nullable=True,
        info={"help_text": "An nD feature vector per image / frame of varying dimensionality according to the chosen descriptor settings."},
    )

    mpeg7_edge_histogram = Column(
        ARRAY(Float),
        nullable=True,
        info={"help_text": "An nD feature vector per image / frame of varying dimensionality according to the chosen descriptor settings."},
    )

    mpeg7_homogeneous_texture = Column(
        ARRAY(Float),
        nullable=True,
        info={"help_text": "An nD feature vector per image / frame of varying dimensionality according to the chosen descriptor settings."},
    )

    mpeg7_scalable_color = Column(
        ARRAY(Float),
        nullable=True,
        info={"help_text": "An nD feature vector per image / frame of varying dimensionality according to the chosen descriptor settings."},
    )

    acquisition = Column(
        Enum(AcquisitionEnum),
        nullable=True,
        # nullable=False,
        info={"help_text": "photo: still images, video: moving images, slide: microscopy images / slide scans"},
    )

    quality = Column(
        Enum(QualityEnum),
        nullable=True,
        # nullable=False,
        info={"help_text": "raw: straight from the sensor, processed: QA/QC'd, product: image data ready for interpretation"},
    )

    deployment = Column(
        Enum(DeploymentEnum),
        nullable=True,
        # nullable=False,
        info={
            "help_text": (
                "mapping: planned path execution along 2-3 spatial axes, stationary: fixed spatial position, "
                "survey: planned path execution along free path, exploration: unplanned path execution, "
                "experiment: observation of manipulated environment, sampling: ex-situ imaging of samples taken "
                "by other method"
            )
        },
    )

    navigation = Column(
        Enum(NavigationEnum),
        nullable=True,
        # nullable=False,
        info={
            "help_text": (
                "satellite: GPS/Galileo etc., beacon: USBL etc., transponder: LBL etc., reconstructed: position "
                "estimated from other measures like cable length and course over ground"
            )
        },
    )

    scale_reference = Column(
        Enum(ScaleReferenceEnum),
        nullable=True,
        # nullable=False,
        info={
            "help_text": (
                "3D camera: the imaging system provides scale directly, calibrated camera: image data and additional "
                "external data like object distance provide scale together, laser marker: scale information is embedded "
                "in the visual data, optical flow: scale is computed from the relative movement of the images and the "
                "camera navigation data"
            )
        },
    )
    illumination = Column(
        Enum(IlluminationEnum),
        nullable=True,
        # nullable=False,
        info={
            "help_text": (
                "sunlight: the scene is only illuminated by the sun, artificial light: the scene is only illuminated "
                "by artificial light, mixed light: both sunlight and artificial light illuminate the scene"
            )
        },
    )

    pixel_magnitude = Column(
        Enum(PixelMagnitudeEnum),
        nullable=True,
        # nullable=False,
        info={"help_text": "average size of one pixel of an image, e.g. km, hm, dam, m, cm, mm, um"},
    )

    marine_zone = Column(
        Enum(MarineZoneEnum),
        nullable=True,
        # nullable=False,
        info={
            "help_text": (
                "seafloor: images taken in/on/right above the seafloor, water column: images taken in the free water "
                "without the seafloor or the sea surface in sight, sea surface: images taken right below the sea surface, "
                "atmosphere: images taken outside of the water, laboratory: images taken ex-situ"
            )
        },
    )

    spectral_resolution = Column(
        Enum(SpectralResEnum),
        nullable=True,
        # nullable=False,
        info={
            "help_text": (
                "grayscale: single channel imagery, rgb: three channel imagery, multi-spectral: 4-10 channel imagery, "
                "hyper-spectral: 10+ channel imagery"
            )
        },
    )

    capture_mode = Column(
        Enum(CaptureModeEnum),
        nullable=True,
        # nullable=False,
        info={"help_text": "whether the time points of image capture were systematic, human-triggered or both"},
    )

    fauna_attraction = Column(
        Enum(FaunaAttractionEnum),
        nullable=True,
        # nullable=False,
        info={"help_text": "Allowed: none, baited, light"},
    )

    area_square_meters = Column(
        Float,
        nullable=True,
        # nullable=False,
        info={
            "help_text": (
                "The footprint of the entire image in square meters. This is the area that the images cover on the seafloor or in the water column."
            )
        },
    )

    meters_above_ground = Column(
        Float,
        nullable=True,
        info={
            "help_text": "Distance of the camera to the seafloor in meters. This is the average distance of the camera to the ground or sea surface."
        },
    )

    acquisition_settings = Column(
        JSONB,
        nullable=True,
        info={"help_text": "All the information that is recorded by the camera in the EXIF, IPTC etc. As a dict. Includes ISO, aperture, etc."},
    )

    camera_yaw_degrees = Column(
        Float,
        nullable=True,
        info={
            "help_text": (
                "Camera view yaw angle. Rotation of camera coordinates (x,y,z = top, right, line of sight) with "
                "respect to NED coordinates (x,y,z = north,east,down) in accordance with the yaw,pitch,roll rotation "
                "order convention: 1. yaw around z, 2. pitch around rotated y, 3. roll around rotated x. Rotation "
                'directions according to "right-hand rule". I.e. for yaw,pitch,roll = 0,0,0 camera is facing downward '
                "with top side towards north."
            )
        },
    )

    camera_pitch_degrees = Column(
        Float,
        nullable=True,
        info={
            "help_text": (
                "Camera view pitch angle. Rotation of camera coordinates (x,y,z = top, right, line of sight) with "
                "respect to NED coordinates (x,y,z = north,east,down) in accordance with the yaw,pitch,roll rotation "
                "order convention: 1. yaw around z, 2. pitch around rotated y, 3. roll around rotated x. Rotation "
                'directions according to "right-hand rule". I.e. for yaw,pitch,roll = 0,0,0 camera is facing downward '
                "with top side towards north."
            )
        },
    )

    camera_roll_degrees = Column(
        Float,
        nullable=True,
        info={
            "help_text": (
                "Camera view roll angle. Rotation of camera coordinates (x,y,z = top, right, line of sight) with "
                "respect to NED coordinates (x,y,z = north,east,down) in accordance with the yaw,pitch,roll rotation "
                "order convention: 1. yaw around z, 2. pitch around rotated y, 3. roll around rotated x. Rotation "
                'directions according to "right-hand rule". I.e. for yaw,pitch,roll = 0,0,0 camera is facing downward '
                "with top side towards north."
            )
        },
    )
    overlap_fraction = Column(
        Float,
        nullable=True,
        info={"help_text": "The average overlap of two consecutive images..."},
    )
    objective = Column(Text, info={"help_text": "A general description of the aims and objectives..."})
    target_environment = Column(Text, info={"help_text": "A description of the habitat or environment..."})
    target_timescale = Column(Text, info={"help_text": "A description of the period or temporal environment..."})
    spatial_constraints = Column(Text, info={"help_text": "A description / definition of the spatial extent..."})
    temporal_constraints = Column(Text, info={"help_text": "A description / definition of the temporal extent..."})

    time_synchronisation = Column(Text, info={"help_text": "Synchronisation procedure and time offsets..."})
    item_identification_scheme = Column(Text, info={"help_text": "How the images file names are constructed..."})
    curation_protocol = Column(Text, info={"help_text": "A description of the image and metadata curation..."})
    visual_constraints = Column(Text, info={"help_text": "An explanation how the images might be degraded..."})


class CommonFieldsAll:
    """Common fields for image_sets and images."""

    name = Column(
        String(255),
        nullable=False,
        unique=True,
        info={
            "help_text": (
                "A unique name for the image set, should include image-project, image-event, image-sensor and optionally the purpose of imaging"
            )
        },
    )
    handle = Column(
        String,
        nullable=True,
        # nullable=False,
        info={"help_text": "A Handle URL to point to the landing page of the image_set or image"},
    )

    copyright = Column(
        String(500),
        nullable=True,
        info={"help_text": "Copyright statement or contact person or office"},
    )
    abstract = Column(
        Text,
        nullable=True,
        info={
            "help_text": (
                "500 - 2000 characters describing what, when, where, why and how the data was collected. "
                "Includes general information on the event (aka station, experiment), e.g. overlap between "
                "images/frames, parameters on platform movement, aims, purpose of image capture etc."
            )
        },
    )
