from typing import Annotated
from uuid import UUID
from fastapi import APIRouter
from fastapi import Depends
from fastapi import File
from fastapi import Form
from fastapi import UploadFile
from sqlalchemy.orm import Session
from ifdo_api.api.deps import get_db
from ifdo_api.api.generic_router import add_common_router
from ifdo_api.api.generic_router import generate_crud_router
from ifdo_api.crud.dataset import dataset_crud
from ifdo_api.crud.image import image_crud
from ifdo_api.models.dataset import Dataset
from ifdo_api.schemas.dataset import DatasetFullSchema
from ifdo_api.schemas.dataset import DatasetSchema
from ifdo_api.schemas.dataset import DatasetSimpleSchema
from ifdo_api.schemas.image import ImageSchema
from ifdo_api.utils.ifdo import DataFormat
from ifdo_api.utils.ifdo import validate_ifdo_data

router: APIRouter = generate_crud_router(
    model_crud=dataset_crud,
    schema=DatasetSchema,
    schema_create=DatasetSchema,
    routes=["create", "delete", "update"],
)

router = add_common_router(model_crud=dataset_crud, schema=DatasetSchema, router=router)


@router.get("/", response_model=list[DatasetSchema] | list[DatasetSimpleSchema] | list[DatasetFullSchema], response_model_exclude_none=True)
async def index(db: Annotated[Session, Depends(get_db)], include_images: bool = False) -> list[Dataset]:
    """Get all items.

    Args:
        db (Session): The database session.
        include_images (bool): Whether to include images in the response. Defaults to False.

    Returns:
        list[DatasetSchema]: A list of items.
    """
    return dataset_crud.index(
        db=db,
        include_images=include_images,
    )


@router.get("/{item_id}", response_model=DatasetSchema | DatasetFullSchema, response_model_exclude_none=True)
async def show(item_id: UUID, db: Annotated[Session, Depends(get_db)], include_images: bool = False) -> Dataset:
    """Get an item by its ID.

    Args:
        item_id (UUID): The ID of the item to retrieve.
        db (Session): The database session.
        include_images (bool): Whether to include images in the response. Defaults to False.

    Raises:
        HTTPException: If the item is not found.

    Returns:
        schema: The item with the specified ID.
    """
    return dataset_crud.show(db=db, id_pk=item_id, include_images=include_images)

    # Handle the include_images parameter


@router.post("/{item_id}/images/", response_model=ImageSchema)
async def add_image_with_body(item_id: UUID, image: ImageSchema | None, db: Annotated[Session, Depends(get_db)]) -> Dataset:
    """Add a image to an image.

    Args:
        item_id (UUID): The ID of the item to which the image is being added.
        image (ImageSchema | None): The image data to be added.
        db (Session): The database session.

    Raises:
        HTTPException: If the creation fails.

    Returns:
        ImageSchema: The created item.
    """
    return dataset_crud.add_image(db=db, crud=image_crud, item_id=item_id, image=image)


@router.post("/{dataset_id}/images/{image_id}", response_model=ImageSchema)
async def add_image(dataset_id: UUID, image_id: UUID, db: Annotated[Session, Depends(get_db)]) -> Dataset:
    """Add a image to a dataset.

    Args:
        dataset_id (UUID): The ID of the dataset to which the image is being added.
        image_id (UUID): The ID of the image being added.
        db (Session): The database session.

    Raises:
        HTTPException: If the creation fails.

    Returns:
        ImageSchema: The created item.
    """
    return dataset_crud.add_image(db=db, crud=image_crud, item_id=dataset_id, image_id=image_id)


@router.post("/ifdo/{data_format}", response_model=DatasetSchema)
async def import_ifdo(
    data_format: DataFormat,
    db: Annotated[Session, Depends(get_db)],
    input_data: Annotated[str | None, Form()] = None,
    input_file: Annotated[UploadFile | None, File()] = None,
) -> DatasetSchema:
    """Import data from IFDO format and create a dataset.

    Args:
        data_format (DataFormat): The format of the IFDO data to import.
        db (Session): The database session.
        input_data (dict | None): An optional dictionary containing IFDO data.
        input_file (UploadFile | None): An optional file containing IFDO data in JSON format.

    Raises:
        HTTPException: If the input data is invalid or if the file format is incorrect.

    Returns:
        schema: The created item.
    """
    input_data = await validate_ifdo_data(data_format, input_data, input_file)

    return dataset_crud.create_from_ifdo(ifdo_data=input_data, db=db)
