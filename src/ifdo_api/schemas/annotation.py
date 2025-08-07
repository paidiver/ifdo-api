from datetime import datetime
from typing import Literal
from pydantic import BaseModel
from pydantic import Field

ShapeType = Literal["single-pixel", "polyline", "polygon", "circle", "rectangle", "ellipse", "whole-image"]


class LabelSchema(BaseModel):
    """A semantic label that can be assigned to an annotation."""

    id: str = Field(..., description="A unique identifier to a semantic label")
    name: str = Field(..., description="A human-readable name for the semantic label")
    info: str | None = Field(None, description="A description on what this semantic label represents")


class AnnotatorSchema(BaseModel):
    """An annotator is a person or machine that creates annotations."""

    id: str = Field(..., description="A unique identifier to an annotation creator, e.g. orcid URL or handle to ML model")
    name: str = Field(..., description="A human-readable name for the annotator (identifying the specific human or machine)")


class AnnotationLabelSchema(BaseModel):
    """A label assigned to an annotation by an annotator."""

    label_id: str = Field(..., description="A unique identifier to a semantic label")
    annotator_id: str = Field(..., description="A unique identifier to an annotation creator, e.g. orcid URL or handle to ML model")
    created_at: datetime = Field(..., description="The date-time stamp of label creation")
    confidence: float | None = Field(
        None,
        ge=0.0,
        le=1.0,
        description="A numerical confidence estimate of the validity of the label between 0 (untrustworthy) and 1 (100% certainty)",
    )


class ImageAnnotationSchema(BaseModel):
    """An annotation is a description of a specific part of an image or video."""

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
    labels: list[AnnotationLabelSchema] = Field(..., description="The list of labels assigned to annotations by annotators")
