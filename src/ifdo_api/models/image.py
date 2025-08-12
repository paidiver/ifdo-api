from geoalchemy2.shape import from_shape
from shapely.geometry import Point
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Table
from sqlalchemy.orm import relationship
from ifdo_api.models.base import Base
from ifdo_api.models.base import DefaultColumns
from ifdo_api.models.common_fields import CommonFields

images_creators = Table(
    "images_creators",
    Base.metadata,
    Column("image_id", ForeignKey("images.id", ondelete="CASCADE"), primary_key=True),
    Column("creator_id", ForeignKey("image_creators.id", ondelete="CASCADE"), primary_key=True),
)


class Image(DefaultColumns, CommonFields, Base):
    """This class represents an image in the database."""

    def __init__(self, **kwargs):  # noqa: ANN003
        super().__init__(**kwargs)
        self._update_geom()

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

    camera_pose_id = Column(ForeignKey("image_camera_poses.id"), nullable=True)
    camera_housing_viewport_id = Column(ForeignKey("image_camera_housing_viewports.id"), nullable=True)
    flatport_parameter_id = Column(ForeignKey("image_flatport_parameters.id"), nullable=True)
    domeport_parameter_id = Column(ForeignKey("image_domeport_parameters.id"), nullable=True)
    photometric_calibration_id = Column(ForeignKey("image_photometric_calibrations.id"), nullable=True)
    camera_calibration_model_id = Column(ForeignKey("image_camera_calibration_models.id"), nullable=True)

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
        ForeignKey("datasets.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
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

    def _update_geom(self) -> None:
        if self.latitude is not None and self.longitude is not None:
            self.geom = from_shape(Point(self.longitude, self.latitude), srid=4326)

    def get_merged_field(self, field_name: str) -> any:
        """Returns image.field or dataset.field if image.field is None.

        Args:
            field_name (str): The name of the field to retrieve.

        Returns:
            any: The value of the field from the image or dataset, or None if not found.
        """
        value = getattr(self, field_name)
        if value is not None and value not in ([], {}, ""):
            return value
        if self.dataset and hasattr(self.dataset, field_name):
            value = getattr(self.dataset, field_name)
            # if isinstance(value, Base):
            #     return value.to_dict()
        return value

    def to_merged_dict(self) -> dict:
        """Returns a dict with fallback values applied.

        Returns:
            dict: A dictionary representation of the image with fallback values applied.
        """
        common_fields = [
            "handle",
            "context_id",
            "project_id",
            "event_id",
            "platform_id",
            "sensor_id",
            "pi_id",
            "license_id",
            "creators",
            "camera_pose_id",
            "camera_housing_viewport_id",
            "flatport_parameter_id",
            "domeport_parameter_id",
            "camera_calibration_model_id",
            "photometric_calibration_id",
            "sha256_hash",
            "date_time",
            "geom",
            "latitude",
            "longitude",
            "altitude_meters",
            "coordinate_uncertainty_meters",
            "copyright",
            "abstract",
            "entropy",
            "particle_count",
            "average_color",
            "mpeg7_color_layout",
            "mpeg7_color_statistic",
            "mpeg7_color_structure",
            "mpeg7_dominant_color",
            "mpeg7_edge_histogram",
            "mpeg7_homogeneous_texture",
            "mpeg7_scalable_color",
            "acquisition",
            "quality",
            "deployment",
            "navigation",
            "scale_reference",
            "illumination",
            "pixel_magnitude",
            "marine_zone",
            "spectral_resolution",
            "capture_mode",
            "fauna_attraction",
            "area_square_meters",
            "meters_above_ground",
            "acquisition_settings",
            "camera_yaw_degrees",
            "camera_pitch_degrees",
            "camera_roll_degrees",
            "overlap_fraction",
            "objective",
            "target_environment",
            "target_timescale",
            "spatial_constraints",
            "temporal_constraints",
            "time_synchronisation",
            "item_identification_scheme",
            "curation_protocol",
            "visual_constraints",
        ]
        image = {field: self.get_merged_field(field) for field in common_fields}
        image["id"] = self.id
        image["name"] = self.name
        image["dataset_id"] = self.dataset_id
        return image

    def __str__(self):
        return self.name
