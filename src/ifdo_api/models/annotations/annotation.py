from sqlalchemy import Column
from sqlalchemy import Enum
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship
from ifdo_api.models.base import Base
from ifdo_api.models.base import DefaultColumns
from ifdo_api.models.base import ShapeEnum


class Annotator(DefaultColumns, Base):
    """An annotator is a person or machine that creates annotations."""

    __tablename__ = "annotators"
    name = Column(
        String(255),
        nullable=False,
        unique=True,
        info={"help": "A human-readable name for the annotator (identifying the specific human or machine)"},
    )

    annotation_labels = relationship(
        "AnnotationLabel",
        back_populates="annotator",
        info={"help_text": "The annotation labels created by this annotator"},
    )


class Annotation(DefaultColumns, Base):
    """An annotation is a description of a specific part of an image or video."""

    __tablename__ = "annotations"

    image_id = Column(
        ForeignKey("images.id", ondelete="CASCADE"),
        nullable=False,
        info={"help": "A unique identifier to the image this annotation belongs to"},
    )

    image = relationship(
        "Image",
        back_populates="annotations",
        info={"help": "The image this annotation belongs to"},
    )

    annotation_platform = Column(
        String(255),
        nullable=True,
        info={"help": "The platform used to create the annotation, e.g., 'BIIGLE', 'VARS', 'SQUIDLE+', none"},
    )

    shape = Column(
        Enum(ShapeEnum),
        nullable=False,
        info={"help": "The annotation shape is specified by a keyword."},
    )

    coordinates = Column(
        JSONB,
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
        back_populates="annotation",
        info={"help_text": "The annotation labels assigned to this annotation"},
    )

    labels = association_proxy("annotation_labels", "label")

    annotation_set_id = Column(
        ForeignKey("annotation_sets.id", ondelete="CASCADE"),
        nullable=False,
        info={"help": "The annotation set this annotation belongs to"},
    )

    annotation_set = relationship(
        "AnnotationSet",
        back_populates="annotations",
        info={"help": "The annotation set this annotation belongs to"},
    )


class AnnotationLabel(DefaultColumns, Base):
    """A label assigned to an annotation by an annotator."""

    __tablename__ = "annotation_labels"

    label_id = Column(
        ForeignKey("labels.id", ondelete="CASCADE"),
        nullable=False,
        info={"help": "A unique identifier to a semantic label"},
    )

    annotation_id = Column(
        ForeignKey("annotations.id", ondelete="CASCADE"),
        nullable=False,
        info={"help": "A unique identifier to the annotation this label is assigned to"},
    )

    annotator_id = Column(
        ForeignKey("annotators.id", ondelete="SET NULL"),
        nullable=True,
        info={"help": "A unique identifier to an annotation creator, e.g. orcid URL or handle to ML model"},
    )
    # confidence = Column(
    #     Float,
    #     nullable=True,
    #     info={"help": "A numerical confidence estimate of the validity of the label between 0 (untrustworthy) and 1 (100% certainty)"},
    # )

    creation_datetime = Column(
        String,
        nullable=False,
        info={"help": "The date-time stamp of label creation"},
    )

    label = relationship("Label", backref="annotation_labels")
    annotator = relationship("Annotator", backref="annotation_labels")
