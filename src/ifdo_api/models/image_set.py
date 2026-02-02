from geoalchemy2 import Geometry
from geoalchemy2.shape import from_shape
from shapely.geometry import Point
from shapely.geometry import box
from sqlalchemy import Column
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy.orm import relationship
from ifdo_api.models.annotations.annotation_set import annotation_set_image_sets
from ifdo_api.models.base import Base
from ifdo_api.models.base import DefaultColumns
from ifdo_api.models.common_fields import CommonFieldsAll
from ifdo_api.models.common_fields import CommonFieldsImagesImageSets
from ifdo_api.models.image import Image

# association tables for many-to-many fields
image_set_creators = Table(
    "image_set_creators",
    Base.metadata,
    Column("image_set_id", ForeignKey("image_sets.id", ondelete="CASCADE"), primary_key=True),
    Column("creator_id", ForeignKey("creators.id", ondelete="CASCADE"), primary_key=True),
)

image_set_related_materials = Table(
    "image_set_related_materials",
    Base.metadata,
    Column("image_set_id", ForeignKey("image_sets.id", ondelete="CASCADE"), primary_key=True),
    Column("material_id", ForeignKey("related_materials.id", ondelete="CASCADE"), primary_key=True),
)


class ImageSet(CommonFieldsAll, CommonFieldsImagesImageSets, DefaultColumns, Base):
    """A collection of images, videos, or other media files that are related to a specific project, event, or context."""

    def __init__(self, **kwargs):  # noqa: ANN003
        super().__init__(**kwargs)
        self._update_geom()
        self._update_limits()

    __tablename__ = "image_sets"
    context_id = Column(
        ForeignKey("contexts.id", onupdate="CASCADE", ondelete="SET NULL"),
        nullable=True,
        info={"help_text": "The overarching project context within which the image set was created"},
    )
    project_id = Column(
        ForeignKey("projects.id", onupdate="CASCADE", ondelete="SET NULL"),
        nullable=True,
        info={"help_text": "The more specific project or expedition or cruise or experiment or ... within which the image set was created."},
    )
    event_id = Column(
        ForeignKey("events.id", onupdate="CASCADE", ondelete="SET NULL"),
        nullable=True,
        info={"help_text": "One event of a project or expedition or cruise or experiment or ... that led to the creation of this image set."},
    )
    platform_id = Column(
        ForeignKey("platforms.id", onupdate="CASCADE", ondelete="SET NULL"),
        nullable=True,
        info={"help_text": "A URI pointing to a description of the camera platform used to create this image set"},
    )
    sensor_id = Column(
        ForeignKey("sensors.id", onupdate="CASCADE", ondelete="SET NULL"),
        nullable=True,
        info={"help_text": "A URI pointing to a description of the sensor used to create this image set."},
    )
    pi_id = Column(
        ForeignKey("pis.id", onupdate="CASCADE", ondelete="SET NULL"),
        nullable=True,
        info={"help_text": "A URI pointing to a description of the principal investigator of the image set"},
    )
    license_id = Column(
        ForeignKey("licenses.id", onupdate="CASCADE", ondelete="SET NULL"),
        nullable=True,
        info={"help_text": "A URI pointing to the license to use the data (should be FAIR, e.g. **CC-BY** or CC-0)"},
    )

    context = relationship("Context", foreign_keys=[context_id], back_populates="image_sets", passive_deletes=True)
    project = relationship("Project", foreign_keys=[project_id], back_populates="image_sets", passive_deletes=True)
    event = relationship("Event", foreign_keys=[event_id], back_populates="image_sets", passive_deletes=True)
    platform = relationship("Platform", foreign_keys=[platform_id], back_populates="image_sets", passive_deletes=True)
    sensor = relationship("Sensor", foreign_keys=[sensor_id], back_populates="image_sets", passive_deletes=True)
    pi = relationship("PI", foreign_keys=[pi_id], back_populates="image_sets", passive_deletes=True)
    license = relationship("License", foreign_keys=[license_id], back_populates="image_sets", passive_deletes=True)

    creators = relationship(
        "Creator",
        secondary=image_set_creators,
        back_populates="image_sets",
        info={"help_text": "Information to identify the creators of the image set"},
    )

    camera_pose_id = Column(ForeignKey("image_camera_poses.id"), nullable=True)
    camera_housing_viewport_id = Column(ForeignKey("image_camera_housing_viewports.id"), nullable=True)
    flatport_parameter_id = Column(ForeignKey("image_flatport_parameters.id"), nullable=True)
    domeport_parameter_id = Column(ForeignKey("image_domeport_parameters.id"), nullable=True)
    photometric_calibration_id = Column(ForeignKey("image_photometric_calibrations.id"), nullable=True)
    camera_calibration_model_id = Column(ForeignKey("image_camera_calibration_models.id"), nullable=True)

    camera_pose = relationship("ImageCameraPose", foreign_keys=[camera_pose_id], back_populates="image_sets", passive_deletes=True)
    camera_housing_viewport = relationship(
        "ImageCameraHousingViewport", foreign_keys=[camera_housing_viewport_id], back_populates="image_sets", passive_deletes=True
    )
    flatport_parameter = relationship(
        "ImageFlatportParameter", foreign_keys=[flatport_parameter_id], back_populates="image_sets", passive_deletes=True
    )
    domeport_parameter = relationship(
        "ImageDomeportParameter", foreign_keys=[domeport_parameter_id], back_populates="image_sets", passive_deletes=True
    )

    camera_calibration_model = relationship(
        "ImageCameraCalibrationModel", back_populates="image_sets", foreign_keys=[camera_calibration_model_id], passive_deletes=True
    )
    photometric_calibration = relationship(
        "ImagePhotometricCalibration", back_populates="image_sets", foreign_keys=[photometric_calibration_id], passive_deletes=True
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
        nullable=True,
        info={"help_text": "Geographic bounding box of the image_set in WGS84 coordinates."},
    )

    related_materials = relationship("RelatedMaterial", secondary=image_set_related_materials, back_populates="image_sets")

    images = relationship(
        "Image",
        foreign_keys=[Image.image_set_id],
        back_populates="image_set",
        cascade="all, delete-orphan",
        passive_deletes=True,
        info={"help_text": "The images that are part of this image_set. This is a one-to-many relationship."},
    )

    annotation_sets = relationship(
        "AnnotationSet",
        secondary=annotation_set_image_sets,
        back_populates="image_sets",
        info={"help_text": "Relationship to annotation sets that include this image_set."},
    )

    # @property
    # def annotations(self) -> list:
    #     """Retrieve all annotations from all images in the image_set."""
    #     return [ann for image in self.images for ann in getattr(image, "annotations", [])]

    # @property
    # def annotation_labels(self) -> list:
    #     """Retrieve all unique labels from all annotations in the image_set."""
    #     return list(
    #         {
    #             label
    #             for image in self.images
    #             for annotation in getattr(image, "annotations", [])
    #             for label in getattr(annotation, "annotation_labels", [])
    #         }
    #     )

    # @property
    # def annotation_set_creators(self) -> list:
    #     """Retrieve all unique creators from all annotations in the image_set."""
    #     return list(
    #         {
    #             creator
    #             for image in self.images
    #             for annotation in getattr(image, "annotations", [])
    #             for creator in getattr(annotation, "annotation_set_creators", [])
    #         }
    #     )

    def _update_geom(self) -> None:
        if self.latitude is not None and self.longitude is not None:
            self.geom = from_shape(Point(self.longitude, self.latitude), srid=4326)

    def _update_limits(self) -> None:
        if (
            self.min_latitude_degrees is not None
            and self.max_latitude_degrees is not None
            and self.min_longitude_degrees is not None
            and self.max_longitude_degrees is not None
        ):
            bbox = box(self.min_longitude_degrees, self.min_latitude_degrees, self.max_longitude_degrees, self.max_latitude_degrees)
            self.limits = from_shape(bbox, srid=4326)

    # @validates("latitude", "longitude")
    # def validate_location(self, key, value):
    #     setattr(self, key, value)
    #     self._update_geom()
    #     return value

    # @validates("min_latitude_degrees", "max_latitude_degrees", "min_longitude_degrees", "max_longitude_degrees")
    # def validate_limits(self, key, value):
    #     setattr(self, key, value)
    #     self._update_limits()
    #     return value

    # @validates("latitude", "longitude")
    # def _update_geom(self, key: str, value: float) -> float:
    #     """Update the location based on latitude and longitude.

    #     Args:
    #         key (str): The key being validated (latitude or longitude).
    #         value (float): The value being set for the key.

    #     Returns:
    #         float: The validated value for the key.
    #     """
    #     if (key == "latitude" and value is not None and self.longitude is not None) or (
    #         key == "longitude" and value is not None and self.latitude is not None
    #     ):
    #         lat = value if key == "latitude" else self.latitude
    #         lon = value if key == "longitude" else self.longitude
    #         self.geom = from_shape(Point(lon, lat), srid=4326)

    #     return value

    # @validates("min_latitude_degrees", "max_latitude_degrees", "min_longitude_degrees", "max_longitude_degrees")
    # def _update_limits(self, key: str, value: float) -> float:
    #     """Update the limits based on bounding box coordinates.

    #     Args:
    #         key (str): The key being validated (min/max latitude/longitude).
    #         value (float): The value being set for the key.

    #     Returns:
    #         float: The validated value for the key.
    #     """
    #     # Only update the limits if all coordinates are available
    #     if (
    #         (key == "min_latitude_degrees" and value is not None and self.min_latitude_degrees is not None)
    #         or (key == "max_latitude_degrees" and value is not None and self.max_latitude_degrees is not None)
    #         or (key == "min_longitude_degrees" and value is not None and self.min_longitude_degrees is not None)
    #         or (key == "max_longitude_degrees" and value is not None and self.max_longitude_degrees is not None)
    #     ):
    #         min_longitude_degrees = value if key == "min_longitude_degrees" else self.min_longitude_degrees
    #         max_longitude_degrees = value if key == "max_longitude_degrees" else self.max_longitude_degrees
    #         min_latitude_degrees = value if key == "min_latitude_degrees" else self.min_latitude_degrees
    #         max_latitude_degrees = value if key == "max_latitude_degrees" else self.max_latitude_degrees
    #         # Create a bounding box polygon
    #         bbox = box(min_longitude_degrees, min_latitude_degrees, max_longitude_degrees, max_latitude_degrees)
    #         self.limits = from_shape(bbox, srid=4326)

    #     return value


# @listens_for(ImageSet, "before_update")
# def set_limits_before_update(mapper, connection, target) -> None:
#     if (
#         target.min_latitude_degrees is not None
#         and target.max_latitude_degrees is not None
#         and target.min_longitude_degrees is not None
#         and target.max_longitude_degrees is not None
#     ):
#         bbox = box(target.min_longitude_degrees, target.min_latitude_degrees, target.max_longitude_degrees, target.max_latitude_degrees)
#         target.limits = from_shape(bbox, srid=4326)
