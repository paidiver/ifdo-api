from geoalchemy2 import Geometry
from geoalchemy2.shape import from_shape
from shapely.geometry import Point
from shapely.geometry import box
from sqlalchemy import Column
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy.orm import relationship
from sqlalchemy.orm import validates
from ifdo_api.models.base import Base
from ifdo_api.models.base import DefaultColumns
from ifdo_api.models.common_fields import CommonFields
from ifdo_api.models.image import Image

# association tables for many-to-many fields
datasets_creators = Table(
    "datasets_creators",
    Base.metadata,
    Column("dataset_id", Integer, ForeignKey("datasets.id"), primary_key=True),
    Column("creator_id", Integer, ForeignKey("image_creators.id"), primary_key=True),
)

dataset_related_material = Table(
    "dataset_related_materials",
    Base.metadata,
    Column("dataset_id", Integer, ForeignKey("datasets.id"), primary_key=True),
    Column("material_id", Integer, ForeignKey("image_set_related_materials.id"), primary_key=True),
)

dataset_provenance_agents = Table(
    "dataset_provenance_agents",
    Base.metadata,
    Column("dataset_id", Integer, ForeignKey("datasets.id"), primary_key=True),
    Column("agent_id", Integer, ForeignKey("provenance_agents.id"), primary_key=True),
)

dataset_provenance_entities = Table(
    "dataset_provenance_entities",
    Base.metadata,
    Column("dataset_id", Integer, ForeignKey("datasets.id"), primary_key=True),
    Column("entity_id", Integer, ForeignKey("provenance_entities.id"), primary_key=True),
)

dataset_provenance_activities = Table(
    "dataset_provenance_activities",
    Base.metadata,
    Column("dataset_id", Integer, ForeignKey("datasets.id"), primary_key=True),
    Column("activity_id", Integer, ForeignKey("provenance_activities.id"), primary_key=True),
)


class Dataset(CommonFields, DefaultColumns, Base):
    """A collection of images, videos, or other media files that are related to a specific project, event, or context."""

    __tablename__ = "datasets"
    handle = Column(
        String,
        nullable=False,
        info={"help_text": "A Handle URL to point to the landing page of the data set"},
    )

    context_id = Column(
        ForeignKey("image_contexts.id", onupdate="CASCADE", ondelete="SET NULL"),
        nullable=True,
        info={"help_text": "The overarching project context within which the image set was created"},
    )
    project_id = Column(
        ForeignKey("image_projects.id", onupdate="CASCADE", ondelete="SET NULL"),
        nullable=True,
        info={"help_text": "The more specific project or expedition or cruise or experiment or ... within which the image set was created."},
    )
    event_id = Column(
        ForeignKey("image_events.id", onupdate="CASCADE", ondelete="SET NULL"),
        nullable=True,
        info={"help_text": "One event of a project or expedition or cruise or experiment or ... that led to the creation of this image set."},
    )
    platform_id = Column(
        ForeignKey("image_platforms.id", onupdate="CASCADE", ondelete="SET NULL"),
        nullable=True,
        info={"help_text": "A URI pointing to a description of the camera platform used to create this image set"},
    )
    sensor_id = Column(
        ForeignKey("image_sensors.id", onupdate="CASCADE", ondelete="SET NULL"),
        nullable=True,
        info={"help_text": "A URI pointing to a description of the sensor used to create this image set."},
    )
    pi_id = Column(
        ForeignKey("image_pis.id", onupdate="CASCADE", ondelete="SET NULL"),
        nullable=True,
        info={"help_text": "A URI pointing to a description of the principal investigator of the image set"},
    )
    license_id = Column(
        ForeignKey("image_licenses.id", onupdate="CASCADE", ondelete="SET NULL"),
        nullable=True,
        info={"help_text": "A URI pointing to the license to use the data (should be FAIR, e.g. **CC-BY** or CC-0)"},
    )

    context = relationship("ImageContext", foreign_keys=[context_id], back_populates="datasets", passive_deletes=True)
    project = relationship("ImageProject", foreign_keys=[project_id], back_populates="datasets", passive_deletes=True)
    event = relationship("ImageEvent", foreign_keys=[event_id], back_populates="datasets", passive_deletes=True)
    platform = relationship("ImagePlatform", foreign_keys=[platform_id], back_populates="datasets", passive_deletes=True)
    sensor = relationship("ImageSensor", foreign_keys=[sensor_id], back_populates="datasets", passive_deletes=True)
    pi = relationship("ImagePI", foreign_keys=[pi_id], back_populates="datasets", passive_deletes=True)
    license = relationship("ImageLicense", foreign_keys=[license_id], back_populates="datasets", passive_deletes=True)

    creators = relationship(
        "ImageCreator",
        secondary=datasets_creators,
        back_populates="datasets",
        info={"help_text": "Information to identify the creators of the image set"},
    )

    camera_pose_id = Column(Integer, ForeignKey("image_camera_poses.id"), nullable=True)
    camera_housing_viewport_id = Column(Integer, ForeignKey("image_camera_housing_viewports.id"), nullable=True)
    flatport_parameter_id = Column(Integer, ForeignKey("image_flatport_parameters.id"), nullable=True)
    domeport_parameter_id = Column(Integer, ForeignKey("image_domeport_parameters.id"), nullable=True)
    photometric_calibration_id = Column(Integer, ForeignKey("image_photometric_calibrations.id"), nullable=True)
    camera_calibration_model_id = Column(Integer, ForeignKey("image_camera_calibration_models.id"), nullable=True)

    camera_pose = relationship("ImageCameraPose", foreign_keys=[camera_pose_id], back_populates="datasets", passive_deletes=True)
    camera_housing_viewport = relationship(
        "ImageCameraHousingViewport", foreign_keys=[camera_housing_viewport_id], back_populates="datasets", passive_deletes=True
    )
    flatport_parameter = relationship("ImageFlatportParameter", foreign_keys=[flatport_parameter_id], back_populates="datasets", passive_deletes=True)
    domeport_parameter = relationship("ImageDomeportParameter", foreign_keys=[domeport_parameter_id], back_populates="datasets", passive_deletes=True)

    camera_calibration_model = relationship(
        "ImageCameraCalibrationModel", back_populates="datasets", foreign_keys=[camera_calibration_model_id], passive_deletes=True
    )
    photometric_calibration = relationship(
        "ImagePhotometricCalibration", back_populates="datasets", foreign_keys=[photometric_calibration_id], passive_deletes=True
    )

    local_path = Column(
        String(500),
        default="../raw",
        nullable=True,
        info={
            "help_text": (
                "Local relative or absolute path to a directory in which (also its sub-directories), the "
                "referenced image files are located. Absolute paths must start with and relative paths without "
                "path separator (ignoring drive letters on windows). The default is the relative path `../raw`."
            )
        },
    )
    min_latitude_degrees = Column(
        Float,
        nullable=True,
        info={"help_text": "The lower bounding box latitude..."},
    )
    max_latitude_degrees = Column(
        Float,
        nullable=True,
        info={"help_text": "The upper bounding box latitude..."},
    )
    min_longitude_degrees = Column(
        Float,
        nullable=True,
        info={"help_text": "The lower bounding box longitude..."},
    )
    max_longitude_degrees = Column(
        Float,
        nullable=True,
        info={"help_text": "The upper bounding box longitude..."},
    )

    limits = Column(
        Geometry(geometry_type="POLYGON", srid=4326),
        nullable=False,
        info={"help_text": "Geographic bounding box of the dataset in WGS84 coordinates."},
    )

    related_materials = relationship("ImageSetRelatedMaterial", secondary=dataset_related_material, back_populates="datasets")
    provenance_agents = relationship("ProvenanceAgent", secondary=dataset_provenance_agents, back_populates="datasets")
    provenance_entities = relationship("ProvenanceEntity", secondary=dataset_provenance_entities, back_populates="datasets")
    provenance_activities = relationship("ProvenanceActivity", secondary=dataset_provenance_activities, back_populates="datasets")

    images = relationship(
        "Image",
        foreign_keys=[Image.dataset_id],
        back_populates="dataset",
        info={"help_text": "The images that are part of this dataset. This is a one-to-many relationship."},
    )

    @property
    def annotations(self) -> list:
        """Retrieve all annotations from all images in the dataset."""
        return [ann for image in self.images for ann in getattr(image, "annotations", [])]

    @property
    def annotation_labels(self) -> list:
        """Retrieve all unique labels from all annotations in the dataset."""
        return list(
            {
                label
                for image in self.images
                for annotation in getattr(image, "annotations", [])
                for label in getattr(annotation, "annotation_labels", [])
            }
        )

    @property
    def annotation_creators(self) -> list:
        """Retrieve all unique creators from all annotations in the dataset."""
        return list(
            {
                creator
                for image in self.images
                for annotation in getattr(image, "annotations", [])
                for creator in getattr(annotation, "annotation_creators", [])
            }
        )

    @validates("latitude", "longitude")
    def _update_location(self, key: str, value: float) -> float:
        """Update the location based on latitude and longitude.

        Args:
            key (str): The key being validated (latitude or longitude).
            value (float): The value being set for the key.

        Returns:
            float: The validated value for the key.
        """
        if (key == "latitude" and value is not None and self.longitude is not None) or (
            key == "longitude" and value is not None and self.latitude is not None
        ):
            lat = value if key == "latitude" else self.latitude
            lon = value if key == "longitude" else self.longitude
            self.location = from_shape(Point(lon, lat), srid=4326)

        return value

    @validates("min_latitude_degrees", "max_latitude_degrees", "min_longitude_degrees", "max_longitude_degrees")
    def _update_limits(self, _: str, value: float) -> float:
        """Update the limits based on bounding box coordinates.

        Args:
            _ (str): The key being validated (min/max latitude/longitude).
            value (float): The value being set for the key.

        Returns:
            float: The validated value for the key.
        """
        # Only update the limits if all coordinates are available
        if (
            self.min_latitude_degrees is not None
            and self.max_latitude_degrees is not None
            and self.min_longitude_degrees is not None
            and self.max_longitude_degrees is not None
        ):
            # Create a bounding box polygon
            bbox = box(self.min_longitude_degrees, self.min_latitude_degrees, self.max_longitude_degrees, self.max_latitude_degrees)
            self.limits = from_shape(bbox, srid=4326)

        return value
