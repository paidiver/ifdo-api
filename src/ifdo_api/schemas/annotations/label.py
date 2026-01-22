from pydantic import BaseModel
from pydantic import Field


class LabelSchema(BaseModel):
    """A semantic label that can be assigned to an annotation."""

    id: str = Field(..., description="A unique identifier to a semantic label")
    name: str = Field(..., description="A human-readable name for the semantic label")
    info: str | None = Field(None, description="A description on what this semantic label represents")
    parent_id: str | None = Field(None, description="The ID of the parent label, if any")
    label_source_id: str | None = Field(None, description="The ID of the source from which this label originates")


class LabelSourceSchema(BaseModel):
    """A source or ontology from which labels are derived."""

    id: str = Field(..., description="A unique identifier to the label source")
    name: str = Field(..., description="A human-readable name for the label source")
    description: str | None = Field(None, description="A description of the label source or ontology")
