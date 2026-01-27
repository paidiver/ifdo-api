from typing import Literal
from pydantic import BaseModel
from pydantic import Field
from ifdo_api.schemas.annotations.label import LabelSchema

ShapeType = Literal["single-pixel", "polyline", "polygon", "circle", "rectangle", "ellipse", "whole-image"]


class AnnotatorSchema(BaseModel):
    """An annotator is a person or machine that creates annotations."""

    id: str = Field(..., description="A unique identifier to an annotation creator, e.g. orcid URL or handle to ML model")
    name: str = Field(..., description="A human-readable name for the annotator (identifying the specific human or machine)")


class AnnotationLabelSchema(BaseModel):
    """A label assigned to an annotation by an annotator."""

    label_id: str = Field(..., description="A unique identifier to a semantic label")
    annotation_id: str = Field(..., description="A unique identifier to the annotation this label is assigned to")
    annotator_id: str = Field(..., description="A unique identifier to an annotation creator, e.g. orcid URL or handle to ML model")
    confidence: float | None = Field(
        None,
        ge=0.0,
        le=1.0,
        description="A numerical confidence estimate of the validity of the label between 0 (untrustworthy) and 1 (100% certainty)",
    )
    creation_datetime: str = Field(..., description="The date-time stamp of label creation")


class AnnotationSchema(BaseModel):
    """An annotation is a description of a specific part of an image or video."""

    image_id: str = Field(..., description="A unique identifier to the image or video this annotation belongs to")

    annotation_platform: str | None = Field(
        None,
        description="The platform used to create the annotation, e.g., 'BIIGLE', 'VARS', 'SQUIDLE+', none",
    )

    shape: ShapeType = Field(..., description="The annotation shape is specified by a keyword.")
    coordinates: list[list[float]] = Field(
        ...,
        description=(
            "The pixel coordinates of one annotation. The top-left corner of an image is the (0,0) coordinate. "
            "The x-axis is the horizontal axis. Pixel coordinates may be fractional. Coordinates are to be given "
            "as a list of lists (only one element for photos, optionally multiple elements for videos). The required "
            "number of pixel coordinates is defined by the shape (0 for whole-image, 2 for single-pixel, 3 for circle, "
            "8 for ellipse/rectangle, 4 or more for polyline, 8 or more for polygon). The third coordinate value of a "
            "circle defines the radius. The first and last coordinates of a polygon must be equal. Format: "
            "[[p1.x,p1.y,p2x,p2.y,...]..]"
        ),
    )
    annotation_labels: list[AnnotationLabelSchema] = Field(..., description="The list of labels assigned to annotations by annotators")
    labels: list[LabelSchema] = Field(..., description="The list of label IDs assigned to this annotation")
