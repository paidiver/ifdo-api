from pydantic import BaseModel


class CatalogSchema(BaseModel):
    """Schema for a image_set model, representing a collection of images and their metadata with full image information."""

    name: str | None = None
    description: str | None = None
    url: str | None = None
