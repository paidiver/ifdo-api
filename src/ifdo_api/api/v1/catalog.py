from typing import Annotated
from fastapi import APIRouter
from fastapi import Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from ifdo_api.api.deps import get_db
from ifdo_api.schemas.catalog import CatalogSchema

router = APIRouter()


@router.get("/", response_model=CatalogSchema)
async def show(db: Annotated[Session, Depends(get_db)]) -> list[BaseModel]:
    """Get an item by its ID.

    Args:
        db (Session): The database session.

    Raises:
        HTTPException: If the item is not found.

    Returns:
        schema: The item with the specified ID.
    """
    _ = db
    return {
        "name": "National Oceanography Centre Catalog",
        "description": "This catalog contains image_sets related to oceanography managed by the National Oceanography Centre.",
        "url": "https://www.bodc.ac.uk/data/published_data_library/",
    }
