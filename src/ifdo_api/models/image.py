from geoalchemy2.shape import from_shape
from shapely.geometry import Point
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Table
from sqlalchemy.orm import relationship
from sqlalchemy.orm import validates
from ifdo_api.models.base import Base
from ifdo_api.models.base import DefaultColumns
from ifdo_api.models.common_fields import CommonFields

images_creators = Table(
    "images_creators",
    Base.metadata,
    Column("image_id", Integer, ForeignKey("images.id"), primary_key=True),
    Column("creator_id", Integer, ForeignKey("image_creators.id"), primary_key=True),
)


class Image(DefaultColumns, CommonFields, Base):
    """This class represents an image in the database."""

    __tablename__ = "images"
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

    context = relationship("ImageContext", foreign_keys=[context_id], back_populates="images", passive_deletes=True)
    project = relationship("ImageProject", foreign_keys=[project_id], back_populates="images", passive_deletes=True)
    event = relationship("ImageEvent", foreign_keys=[event_id], back_populates="images", passive_deletes=True)
    platform = relationship("ImagePlatform", foreign_keys=[platform_id], back_populates="images", passive_deletes=True)
    sensor = relationship("ImageSensor", foreign_keys=[sensor_id], back_populates="images", passive_deletes=True)
    pi = relationship("ImagePI", foreign_keys=[pi_id], back_populates="images", passive_deletes=True)
    license = relationship("ImageLicense", foreign_keys=[license_id], back_populates="images", passive_deletes=True)

    creators = relationship(
        "ImageCreator",
        secondary=images_creators,
        back_populates="images",
        info={"help_text": "Information to identify the creators of the image set"},
    )

    camera_pose_id = Column(Integer, ForeignKey("image_camera_poses.id"), nullable=True)
    camera_housing_viewport_id = Column(Integer, ForeignKey("image_camera_housing_viewports.id"), nullable=True)
    flatport_parameter_id = Column(Integer, ForeignKey("image_flatport_parameters.id"), nullable=True)
    domeport_parameter_id = Column(Integer, ForeignKey("image_domeport_parameters.id"), nullable=True)
    photometric_calibration_id = Column(Integer, ForeignKey("image_photometric_calibrations.id"), nullable=True)
    camera_calibration_model_id = Column(Integer, ForeignKey("image_camera_calibration_models.id"), nullable=True)

    camera_pose = relationship("ImageCameraPose", foreign_keys=[camera_pose_id], back_populates="images", passive_deletes=True)
    camera_housing_viewport = relationship(
        "ImageCameraHousingViewport", foreign_keys=[camera_housing_viewport_id], back_populates="images", passive_deletes=True
    )
    flatport_parameter = relationship("ImageFlatportParameter", foreign_keys=[flatport_parameter_id], back_populates="images", passive_deletes=True)
    domeport_parameter = relationship("ImageDomeportParameter", foreign_keys=[domeport_parameter_id], back_populates="images", passive_deletes=True)

    camera_calibration_model = relationship(
        "ImageCameraCalibrationModel", back_populates="images", foreign_keys=[camera_calibration_model_id], passive_deletes=True
    )
    photometric_calibration = relationship(
        "ImagePhotometricCalibration", back_populates="images", foreign_keys=[photometric_calibration_id], passive_deletes=True
    )

    dataset_id = Column(
        ForeignKey("datasets.uuid", onupdate="CASCADE", ondelete="SET NULL"),
        nullable=True,
        info={"help_text": "The dataset this image belongs to. A dataset can have multiple images."},
    )

    dataset = relationship(
        "Dataset",
        back_populates="images",
        info={"help_text": "The dataset this image belongs to. A dataset can have multiple images."},
        passive_deletes=True,
    )

    annotations = relationship(
        "Annotation",
        back_populates="image",
        cascade="all, delete-orphan",
        info={"help_text": "All the annotations in this image set. Each annotation has a shape, coordinates, and a list of labels assigned to it."},
    )

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

    def get_merged_field(self, field_name: str) -> any:
        """Returns image.field or dataset.field if image.field is None.

        Args:
            field_name (str): The name of the field to retrieve.

        Returns:
            any: The value of the field from the image or dataset, or None if not found.
        """
        value = getattr(self, field_name)
        if value is not None:
            return value
        if self.dataset:
            return getattr(self.dataset, field_name)
        return None

    def to_merged_dict(self) -> dict:
        """Returns a dict with fallback values applied.

        Returns:
            dict: A dictionary representation of the image with fallback values applied.
        """
        return {
            "id": self.id,
            "uuid": self.uuid,
            "dataset_id": self.dataset_id,
            "context_id": self.get_merged_field("context_id"),
            "project_id": self.get_merged_field("project_id"),
            "event_id": self.get_merged_field("event_id"),
            "platform_id": self.get_merged_field("platform_id"),
            "sensor_id": self.get_merged_field("sensor_id"),
            "pi_id": self.get_merged_field("pi_id"),
            "license_id": self.get_merged_field("license_id"),
            "creators": [self.get_merged_field("creators")],
            "camera_pose_id": self.get_merged_field("camera_pose_id"),
            "camera_housing_viewport_id": self.get_merged_field("camera_housing_viewport_id"),
            "flatport_parameter_id": self.get_merged_field("flatport_parameter_id"),
            "domeport_parameter_id": self.get_merged_field("domeport_parameter_id"),
            "camera_calibration_model_id": self.get_merged_field("camera_calibration_model_id"),
            "photometric_calibration_id": self.get_merged_field("photometric_calibration_id"),
            "annotations": [annotation.to_dict() for annotation in self.annotations],
            "annotation_labels": [label.to_dict() for label in self.annotation_labels],
            "annotation_creators": [creator.to_dict() for creator in self.annotation_creators],
            "sha256_hash": self.get_merged_field("sha256_hash"),
            "date_time": self.get_merged_field("date_time"),
            "location": self.get_merged_field("location"),
            "latitude": self.get_merged_field("latitude"),
            "longitude": self.get_merged_field("longitude"),
            "altitude_meters": self.get_merged_field("altitude_meters"),
            "coordinate_uncertainty_m": self.get_merged_field("coordinate_uncertainty_m"),
            "copyright": self.get_merged_field("copyright"),
            "abstract": self.get_merged_field("abstract"),
            "entropy": self.get_merged_field("entropy"),
            "particle_count": self.get_merged_field("particle_count"),
            "average_color": self.get_merged_field("average_color"),
            "mpeg7_color_layout": self.get_merged_field("mpeg7_color_layout"),
            "mpeg7_color_statistic": self.get_merged_field("mpeg7_color_statistic"),
            "mpeg7_color_structure": self.get_merged_field("mpeg7_color_structure"),
            "mpeg7_dominant_color": self.get_merged_field("mpeg7_dominant_color"),
            "mpeg7_edge_histogram": self.get_merged_field("mpeg7_edge_histogram"),
            "mpeg7_homogeneous_texture": self.get_merged_field("mpeg7_homogeneous_texture"),
            "mpeg7_scalable_color": self.get_merged_field("mpeg7_scalable_color"),
            "acquisition": self.get_merged_field("acquisition"),
            "quality": self.get_merged_field("quality"),
            "deployment": self.get_merged_field("deployment"),
            "navigation": self.get_merged_field("navigation"),
            "scale_reference": self.get_merged_field("scale_reference"),
            "illumination": self.get_merged_field("illumination"),
            "pixel_magnitude": self.get_merged_field("pixel_magnitude"),
            "marine_zone": self.get_merged_field("marine_zone"),
            "spectral_resolution": self.get_merged_field("spectral_resolution"),
            "capture_mode": self.get_merged_field("capture_mode"),
            "fauna_attraction": self.get_merged_field("fauna_attraction"),
            "area_square_meters": self.get_merged_field("area_square_meters"),
            "meters_above_ground": self.get_merged_field("meters_above_ground"),
            "acquisition_settings": self.get_merged_field("acquisition_settings"),
            "camera_yaw_degrees": self.get_merged_field("camera_yaw_degrees"),
            "camera_pitch_degrees": self.get_merged_field("camera_pitch_degrees"),
            "camera_roll_degrees": self.get_merged_field("camera_roll_degrees"),
            "overlap_fraction": self.get_merged_field("overlap_fraction"),
            "objective": self.get_merged_field("objective"),
            "target_environment": self.get_merged_field("target_environment"),
            "target_timescale": self.get_merged_field("target_timescale"),
            "spatial_constraints": self.get_merged_field("spatial_constraints"),
            "temporal_constraints": self.get_merged_field("temporal_constraints"),
            "time_synchronisation": self.get_merged_field("time_synchronisation"),
            "item_identification_scheme": self.get_merged_field("item_identification_scheme"),
            "curation_protocol": self.get_merged_field("curation_protocol"),
            "visual_constraints": self.get_merged_field("visual_constraints"),
        }

    def __str__(self):
        return self.name
