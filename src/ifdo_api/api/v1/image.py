from typing import Annotated
from uuid import UUID
from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from ifdo_api.api.deps import get_db
from ifdo_api.api.generic_router import add_common_router
from ifdo_api.api.generic_router import generate_crud_router
from ifdo_api.crud.image import image_crud
from ifdo_api.models.image import Image
from ifdo_api.schemas.image import ImageSchema

router: APIRouter = generate_crud_router(
    model_crud=image_crud, schema=ImageSchema, schema_create=ImageSchema, routes=["create", "delete", "update", "index"]
)

router = add_common_router(model_crud=image_crud, schema=ImageSchema, router=router)


@router.get("/{item_id}", response_model=ImageSchema, response_model_exclude_none=True)
async def show(item_id: UUID, db: Annotated[Session, Depends(get_db)], replace_image_set: bool = False) -> Image:
    """Get an item by its ID.

    Args:
        item_id (UUID): The ID of the item to retrieve.
        db (Session): The database session.
        replace_image_set (bool): Whether to replace the image field with the existing image_set field. Defaults to False.

    Raises:
        HTTPException: If the item is not found.

    Returns:
        schema: The item with the specified ID.
    """
    image = image_crud.show(db=db, id_pk=item_id)
    if replace_image_set:
        return image.to_merged_dict()
    return image

    # Handle the include_images parameter


# @router.post("/{item_id}/annotations/{annotation_id}", response_model=ImageSchema)
# async def add_annotation(item_id: UUID, annotation_id: UUID, db: Annotated[Session, Depends(get_db)]) -> BaseModel:
#     """Add a annotation to an image.

#     Args:
#         item_id (UUID): The ID of the item to which the annotation is being added.
#         annotation_id (UUID): The ID of the annotation being added.
#         db (Session): The database session.

#     Raises:
#         HTTPException: If the creation fails.

#     Returns:
#         ImageSchema: The created item.
#     """
#     return image_crud.add_annotation(db=db, item_id=item_id, annotation_id=annotation_id)


# @router.post("/{item_id}/annotations/", response_model=ImageSchema)
# async def add_new_annotation(item_id: UUID, annotation: ImageCreatorSchema, db: Annotated[Session, Depends(get_db)]) -> BaseModel:
#     """Add new annotation to an image.

#     Args:
#         item_id (UUID): The ID of the item to which the annotation is being added.
#         annotation (ImageCreatorSchema): The annotation data to be added.
#         db (Session): The database session.

#     Raises:
#         HTTPException: If the creation fails.

#     Returns:
#         ImageSchema: The created item.
#     """
#     new_annotation = ImageCreatorSchema(**annotation.model_dump(exclude_unset=True))
#     created_item = annotation_crud.create(db=db, obj_in=new_annotation)
#     if not created_item:
#         raise HTTPException(status_code=404, detail="Creation failed")
#     return image_crud.add_annotation(db=db, item_id=item_id, annotation_id=created_item.uuid)
