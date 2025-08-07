import enum
from sqlalchemy import Column
from sqlalchemy import Enum
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy import Text
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship
from ifdo_api.models.base import Base
from ifdo_api.models.base import DefaultColumns


class ShapeEnum(str, enum.Enum):
    """Enumeration of possible annotation shapes."""

    single_pixel = "single-pixel"
    polyline = "polyline"
    polygon = "polygon"
    circle = "circle"
    rectangle = "rectangle"
    ellipse = "ellipse"
    whole_image = "whole-image"


image_annotation_labels = Table(
    "image_annotation_labels",
    Base.metadata,
    Column("annotation_id", ForeignKey("annotations.id"), primary_key=True),
    Column("annotation_label_id", ForeignKey("annotation_labels.id"), primary_key=True),
)


class Label(DefaultColumns, Base):
    """A semantic label that can be assigned to an annotation."""

    __tablename__ = "labels"
    name = Column(
        String(255),
        nullable=False,
        unique=True,
        info={"help": "A human-readable name for the semantic label"},
    )
    info = Column(
        Text,
        nullable=True,
        info={"help": "A description on what this semantic label represents"},
    )


class Annotator(DefaultColumns, Base):
    """An annotator is a person or machine that creates annotations."""

    __tablename__ = "annotators"
    name = Column(
        String(255),
        nullable=False,
        unique=True,
        info={"help": "A human-readable name for the annotator (identifying the specific human or machine)"},
    )


class AnnotationLabel(DefaultColumns, Base):
    """A label assigned to an annotation by an annotator."""

    __tablename__ = "annotation_labels"

    label_id = Column(
        Integer,
        ForeignKey("labels.id"),
        nullable=False,
        info={"help": "A unique identifier to a semantic label"},
    )
    annotator_id = Column(
        Integer,
        ForeignKey("annotators.id"),
        nullable=False,
        info={"help": "A unique identifier to an annotation creator, e.g. orcid URL or handle to ML model"},
    )
    confidence = Column(
        Float,
        nullable=True,
        info={"help": "A numerical confidence estimate of the validity of the label between 0 (untrustworthy) and 1 (100% certainty)"},
    )

    label = relationship("Label", backref="annotation_labels")
    annotator = relationship("Annotator", backref="annotation_labels")


class Annotation(DefaultColumns, Base):
    """An annotation is a description of a specific part of an image or video."""

    __tablename__ = "annotations"

    shape = Column(
        Enum(ShapeEnum),
        nullable=False,
        info={"help": "The annotation shape is specified by a keyword."},
    )
    coordinates = Column(
        ARRAY(Float, dimensions=2),
        nullable=False,
        info={
            "help": "The pixel coordinates of one annotation. The top-left corner of an image is the (0,0) coordinate. "
            "The x-axis is the horizontal axis. Pixel coordinates may be fractional. Coordinates are to be "
            "given as a list of lists (only one element for photos, optionally multiple elements for videos). "
            "The required number of pixel coordinates is defined by the shape (0 for whole-image, 2 for single-pixel, "
            "3 for circle, 8 for ellipse/rectangle, 4 or more for polyline, 8 or more for polygon). The third coordinate "
            "value of a circle defines the radius. The first and last coordinates of a polygon must be equal. "
            "Format: [[p1.x,p1.y,p2x,p2.y,...]..]"
        },
    )

    annotation_labels = relationship(
        "AnnotationLabel",
        secondary=image_annotation_labels,
        backref="annotations",
        info={"help": "The list of labels assigned to annotations by annotators"},
    )

    labels = association_proxy("annotation_labels", "label")
    creators = association_proxy("annotation_labels", "creator")

    image_id = Column(
        Integer,
        ForeignKey("images.id"),
        nullable=False,
        info={"help": "A unique identifier to the image this annotation belongs to"},
    )

    image = relationship(
        "Image",
        back_populates="annotations",
        info={"help": "The image this annotation belongs to"},
    )
