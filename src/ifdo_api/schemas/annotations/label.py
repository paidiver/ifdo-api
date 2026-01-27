from pydantic import BaseModel
from pydantic import Field


class LabelSchema(BaseModel):
    """A semantic label that can be assigned to an annotation."""

    id: str = Field(..., description="A unique identifier to a semantic label")
    name: str = Field(..., description="A human-readable name for the semantic label")
    group: str = Field(..., description="Grouping or higher taxonomic group of label")
    lowest_taxonomic_name: str | None = Field(None, description="Most detailed taxonomic identification possible; scientificName field in DarwinCore")
    lowest_aphia_id: str | None = Field(None, description="The AphiaID corresponding to the lowest_taxonomic_name, if applicable")
    name_is_lowest: bool = Field(..., description="Indicates whether the name field represents the lowest taxonomic identification")
    identification_qualifier: str | None = Field(None, description="Open nomenclature signs (see Horton et al 2021); same field name in DarwinCore")
    # parent_id: str | None = Field(None, description="The ID of the parent label, if any")
    # label_source_id: str | None = Field(None, description="The ID of the source from which this label originates")


# class LabelSourceSchema(BaseModel):
#     """A source or ontology from which labels are derived."""

#     id: str = Field(..., description="A unique identifier to the label source")
#     name: str = Field(..., description="A human-readable name for the label source")
#     description: str | None = Field(None, description="A description of the label source or ontology")
