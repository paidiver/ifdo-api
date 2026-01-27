from sqlalchemy import Column
from sqlalchemy import Float
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship
from ifdo_api.models.annotations.annotation_set import annotation_set_creators
from ifdo_api.models.base import Base
from ifdo_api.models.base import DefaultColumns
from ifdo_api.models.image import Image
from ifdo_api.models.image import image_creators
from ifdo_api.models.image_set import ImageSet
from ifdo_api.models.image_set import image_set_creators
from ifdo_api.models.image_set import image_set_related_materials


class NamedURI:
    """A mixin class for models that have a name and a URI."""

    name = Column(String(255), unique=True, nullable=False)
    uri = Column(String, nullable=True)


class Context(DefaultColumns, NamedURI, Base):
    """Represents a context in which an image was captured."""

    __tablename__ = "contexts"
    images = relationship(
        "Image",
        foreign_keys=[Image.context_id],
        back_populates="context",
        passive_deletes=True,
    )
    image_sets = relationship(
        "ImageSet",
        foreign_keys=[ImageSet.context_id],
        back_populates="context",
        passive_deletes=True,
    )


class Project(DefaultColumns, NamedURI, Base):
    """Represents a project related to an image."""

    __tablename__ = "projects"
    images = relationship(
        "Image",
        foreign_keys=[Image.project_id],
        back_populates="project",
    )
    image_sets = relationship(
        "ImageSet",
        foreign_keys=[ImageSet.project_id],
        back_populates="project",
        passive_deletes=True,
    )


class Event(DefaultColumns, NamedURI, Base):
    """Represents an event related to an image."""

    __tablename__ = "events"
    images = relationship(
        "Image",
        foreign_keys=[Image.event_id],
        back_populates="event",
        passive_deletes=True,
    )
    image_sets = relationship(
        "ImageSet",
        foreign_keys=[ImageSet.event_id],
        back_populates="event",
        passive_deletes=True,
    )


class Platform(DefaultColumns, NamedURI, Base):
    """Represents a platform on which an image was captured."""

    __tablename__ = "platforms"
    images = relationship(
        "Image",
        foreign_keys=[Image.platform_id],
        back_populates="platform",
        passive_deletes=True,
    )
    image_sets = relationship(
        "ImageSet",
        foreign_keys=[ImageSet.platform_id],
        back_populates="platform",
        passive_deletes=True,
    )


class Sensor(DefaultColumns, NamedURI, Base):
    """Represents a sensor used to capture an image."""

    __tablename__ = "sensors"
    images = relationship(
        "Image",
        foreign_keys=[Image.sensor_id],
        back_populates="sensor",
        passive_deletes=True,
    )
    image_sets = relationship(
        "ImageSet",
        foreign_keys=[ImageSet.sensor_id],
        back_populates="sensor",
        passive_deletes=True,
    )


class PI(DefaultColumns, NamedURI, Base):
    """Represents a principal investigator related to an image."""

    __tablename__ = "pis"
    images = relationship(
        "Image",
        foreign_keys=[Image.pi_id],
        back_populates="pi",
        passive_deletes=True,
    )
    image_sets = relationship(
        "ImageSet",
        foreign_keys=[ImageSet.pi_id],
        back_populates="pi",
        passive_deletes=True,
    )


class Creator(DefaultColumns, NamedURI, Base):
    """Represents a creator of an image."""

    __tablename__ = "creators"
    images = relationship(
        "Image",
        secondary=image_creators,
        back_populates="creators",
        passive_deletes=True,
    )

    image_sets = relationship(
        "ImageSet",
        secondary=image_set_creators,
        back_populates="creators",
        passive_deletes=True,
    )

    annotation_sets = relationship(
        "AnnotationSet",
        secondary=annotation_set_creators,
        back_populates="creators",
        passive_deletes=True,
    )


class License(DefaultColumns, NamedURI, Base):
    """Represents a license under which an image is shared."""

    __tablename__ = "licenses"
    images = relationship(
        "Image",
        foreign_keys=[Image.license_id],
        back_populates="license",
        passive_deletes=True,
    )
    image_sets = relationship(
        "ImageSet",
        foreign_keys=[ImageSet.license_id],
        back_populates="license",
        passive_deletes=True,
    )

    annotation_sets = relationship(
        "AnnotationSet",
        foreign_keys="[AnnotationSet.license_id]",
        back_populates="license",
        passive_deletes=True,
    )


class ImageCameraPose(DefaultColumns, Base):
    """Represents the camera pose information for an image."""

    __tablename__ = "image_camera_poses"
    utm_zone = Column(String(10), nullable=True, info={"help_text": "The UTM zone number"})
    utm_epsg = Column(String(10), nullable=True, info={"help_text": "The EPSG code of the UTM zone"})
    utm_east_north_up_meters = Column(
        ARRAY(Float, dimensions=1), nullable=True, info={"help_text": "The position of the camera center in UTM coordinates."}
    )
    absolute_orientation_utm_matrix = Column(
        ARRAY(Float, dimensions=1),
        nullable=True,
        info={
            "help_text": (
                "3x3 row-major float rotation matrix that transforms a direction in camera coordinates "
                "(x,y,z = right,down,line of sight) into a direction in UTM coordinates "
                "(x,y,z = easting,northing,up)"
            )
        },
    )
    images = relationship(
        "Image",
        foreign_keys=[Image.camera_pose_id],
        back_populates="camera_pose",
        passive_deletes=True,
    )
    image_sets = relationship(
        "ImageSet",
        foreign_keys=[ImageSet.camera_pose_id],
        back_populates="camera_pose",
        passive_deletes=True,
    )


class ImageCameraHousingViewport(DefaultColumns, Base):
    """Represents the camera housing viewport parameters for an image."""

    __tablename__ = "image_camera_housing_viewports"
    viewport_type = Column(String(100), nullable=True, info={"help_text": "e.g.: flat port, dome port, other"})
    optical_density = Column(Float, nullable=True, info={"help_text": "Unit-less optical density (1.0=vacuum)"})
    thickness_millimeters = Column(Float, nullable=True, info={"help_text": "Thickness of viewport in millimeters"})
    extra_description = Column(Text, nullable=True, info={"help_text": "A textual description of the viewport used"})
    images = relationship(
        "Image",
        foreign_keys=[Image.camera_housing_viewport_id],
        back_populates="camera_housing_viewport",
        passive_deletes=True,
    )
    image_sets = relationship(
        "ImageSet",
        foreign_keys=[ImageSet.camera_housing_viewport_id],
        back_populates="camera_housing_viewport",
        passive_deletes=True,
    )


class ImageFlatportParameter(DefaultColumns, Base):
    """Represents the parameters of a flat port used in an image."""

    __tablename__ = "image_flatport_parameters"
    lens_port_distance_millimeters = Column(
        Float,
        nullable=True,
        info={"help_text": "The distance between the front of the camera lens and the inner side of the housing viewport in millimeters."},
    )
    interface_normal_direction = Column(
        ARRAY(Float, dimensions=1),
        nullable=True,
        info={
            "help_text": (
                "3D direction vector to specify how the view direction of the lens intersects with the viewport (unit-less, (0,0,1) is aligned)"
            )
        },
    )
    extra_description = Column(Text, nullable=True, info={"help_text": "A textual description of the flat port used"})
    images = relationship(
        "Image",
        foreign_keys=[Image.flatport_parameter_id],
        back_populates="flatport_parameter",
        passive_deletes=True,
    )
    image_sets = relationship(
        "ImageSet",
        foreign_keys=[ImageSet.flatport_parameter_id],
        back_populates="flatport_parameter",
        passive_deletes=True,
    )


class ImageDomeportParameter(DefaultColumns, Base):
    """Represents the parameters of a dome port used in an image."""

    __tablename__ = "image_domeport_parameters"
    outer_radius_millimeters = Column(
        Float, nullable=True, info={"help_text": "Outer radius of the dome port - the part that has contact with the water."}
    )
    decentering_offset_xyz_millimeters = Column(
        ARRAY(Float, dimensions=1),
        nullable=True,
        info={"help_text": "3D offset vector of the camera center from the dome port center in millimeters"},
    )
    extra_description = Column(Text, nullable=True, info={"help_text": "A textual description of the dome port used"})
    images = relationship(
        "Image",
        foreign_keys=[Image.domeport_parameter_id],
        back_populates="domeport_parameter",
        passive_deletes=True,
    )
    image_sets = relationship(
        "ImageSet",
        foreign_keys=[ImageSet.domeport_parameter_id],
        back_populates="domeport_parameter",
        passive_deletes=True,
    )


class ImageCameraCalibrationModel(DefaultColumns, Base):
    """Represents the camera calibration model parameters for an image."""

    __tablename__ = "image_camera_calibration_models"
    calibration_model_type = Column(
        String(100), nullable=True, info={"help_text": "e.g.: rectilinear air, rectilinear water, fisheye air, fisheye water, other"}
    )
    focal_length_xy_pixel = Column(ARRAY(Float, dimensions=1), nullable=True, info={"help_text": "2D focal length in pixels"})
    principal_point_xy_pixel = Column(
        ARRAY(Float, dimensions=1),
        nullable=True,
        info={"help_text": "2D principal point of the calibration in pixels (top left pixel center is 0,0, x right, y down)"},
    )
    distortion_coefficients = Column(
        ARRAY(Float, dimensions=1), nullable=True, info={"help_text": "rectilinear: k1, k2, p1, p2, k3, k4, k5, k6, fisheye: k1, k2, k3, k4"}
    )
    approximate_field_of_view_water_xy_degree = Column(
        ARRAY(Float, dimensions=1), nullable=True, info={"help_text": "Proxy for pixel to meter conversion, and as backup"}
    )
    extra_description = Column(Text, nullable=True, info={"help_text": "Explain model, or if lens parameters are in mm rather than in pixel"})
    images = relationship(
        "Image",
        foreign_keys=[Image.camera_calibration_model_id],
        back_populates="camera_calibration_model",
        passive_deletes=True,
    )
    image_sets = relationship(
        "ImageSet",
        foreign_keys=[ImageSet.camera_calibration_model_id],
        back_populates="camera_calibration_model",
        passive_deletes=True,
    )


class ImagePhotometricCalibration(DefaultColumns, Base):
    """Represents the photometric calibration parameters for an image."""

    __tablename__ = "image_photometric_calibrations"
    sequence_white_balancing = Column(Text, nullable=True, info={"help_text": "A text on how white-balancing was done."})
    exposure_factor_rgb = Column(
        ARRAY(Float, dimensions=1),
        nullable=True,
        info={"help_text": "RGB factors applied to this image, product of ISO, exposure time, relative white balance"},
    )
    sequence_illumination_type = Column(
        String(100),
        nullable=True,
        info={"help_text": "e.g. constant artificial, globally adapted artificial, individually varying light sources, sunlight, mixed)"},
    )
    sequence_illumination_description = Column(Text, nullable=True, info={"help_text": "A text on how the image sequence was illuminated"})
    illumination_factor_rgb = Column(
        ARRAY(Float, dimensions=1), nullable=True, info={"help_text": "RGB factors applied to artificial lights for this image"}
    )
    water_properties_description = Column(
        Text, nullable=True, info={"help_text": "A text describing the photometric properties of the water within which the images were capture"}
    )
    images = relationship(
        "Image",
        foreign_keys=[Image.photometric_calibration_id],
        back_populates="photometric_calibration",
        passive_deletes=True,
    )
    image_sets = relationship(
        "ImageSet",
        foreign_keys=[ImageSet.photometric_calibration_id],
        back_populates="photometric_calibration",
        passive_deletes=True,
    )


class RelatedMaterial(DefaultColumns, Base):
    """Represents a related material for an image set."""

    __tablename__ = "related_materials"
    uri = Column(String, info={"help_text": "The URI pointing to a related resource"})
    title = Column(String(255), info={"help_text": "A name characterising the resource that is pointed to"})
    relation = Column(Text, info={"help_text": "A textual explanation how this material is related to this image set"})

    image_sets = relationship(
        "ImageSet",
        secondary=image_set_related_materials,
        back_populates="related_materials",
        passive_deletes=True,
    )
