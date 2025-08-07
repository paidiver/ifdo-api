from typing import Annotated
from typing import Generic
from typing import TypeVar
from uuid import UUID
from fastapi import APIRouter
from fastapi import Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from ifdo_api.api.deps import get_db
from ifdo_api.api.exceptions import NotFoundException
from ifdo_api.crud.fields import image_creator_crud
from ifdo_api.schemas.fields import ImageCreatorSchema

T = TypeVar("T")


def generate_crud_router(  # noqa: C901
    model_crud: Generic[T],
    schema: type[BaseModel],
    schema_create: type[BaseModel],
    routes: str | None = None,
    router: APIRouter | None = None,
) -> APIRouter:
    """Generate a CRUD router for the given model and schemas.

    Args:
        model_crud (Generic[Base]): The CRUD operations for the model.
        schema (BaseModel): The Pydantic schema for the model.
        schema_create (BaseModel): The Pydantic schema for creating a new model instance.
        routes (str | None): A string containing the routes to include. If None, all routes are included.
        router (APIRouter | None): An optional FastAPI router to use. If None, a new router will be created.

    Returns:
        APIRouter: A FastAPI router with CRUD endpoints.
    """
    if router is None:
        router = APIRouter()
    model = model_crud.model
    if routes is None:
        routes = ["index", "show", "create", "delete", "update"]

    if "index" in routes:

        @router.get("/", response_model=list[schema])
        async def index(db: Annotated[Session, Depends(get_db)]) -> list[BaseModel]:
            """Get all items.

            Returns:
                list[schema]: A list of items.
            """
            return model_crud.index(db=db)

    if "show" in routes:

        @router.get("/{item_id}", response_model=schema)
        async def show(item_id: UUID, db: Annotated[Session, Depends(get_db)]) -> list[BaseModel]:
            """Get an item by its ID.

            Args:
                item_id (UUID): The ID of the item to retrieve.
                db (Session): The database session.

            Raises:
                HTTPException: If the item is not found.

            Returns:
                schema: The item with the specified ID.
            """
            return model_crud.show(db=db, uuid=item_id)

    if "create" in routes:

        @router.post("/", response_model=schema)
        async def create(obj_in: schema_create, db: Annotated[Session, Depends(get_db)]) -> list[BaseModel]:  # type: ignore[arg-type]
            """Create a new item.

            Args:
                obj_in (schema_create): The data for the new item.
                db (Session): The database session.

            Raises:
                HTTPException: If the creation fails.

            Returns:
                schema: The created item.
            """
            created_item = model_crud.create(db=db, obj_in=obj_in)
            if not created_item:
                raise NotFoundException(model.__name__)

            return created_item

    if "delete" in routes:

        @router.delete("/{item_id}", response_model=schema)
        async def delete(item_id: UUID, db: Annotated[Session, Depends(get_db)]) -> list[BaseModel]:
            """Delete an item by its ID.

            Args:
                item_id (UUID): The ID of the item to delete.
                db (Session): The database session.

            Raises:
                HTTPException: If the item is not found.

            Returns:
                schema: The deleted item.
            """
            return model_crud.delete(db=db, uuid=item_id)

    if "update" in routes:

        @router.put("/{item_id}", response_model=schema)
        async def update(item_id: UUID, update_data: schema_create, db: Annotated[Session, Depends(get_db)]) -> list[BaseModel]:  # type: ignore[arg-type]
            """Update an item.

            Args:
                item_id (UUID): The ID of the item to update.
                update_data (schema_create): The data to update the item with.
                db (Session): The database session.

            Raises:
                HTTPException: If the item is not found.

            Returns:
                schema: The updated item.
            """
            db_item = model_crud.show(db=db, uuid=item_id)
            if not db_item:
                raise NotFoundException(model.__name__)
            return model_crud.update(db=db, id_pk=db_item.id, obj_in=update_data)

    return router


def add_common_router(
    model_crud: Generic[T],
    schema: BaseModel,
    router: APIRouter | None = None,
) -> APIRouter:
    """Generate a CRUD router for the given model and schemas.

    Args:
        model_crud (Generic[Base]): The CRUD operations for the model.
        schema (BaseModel): The Pydantic schema for the model.
        router (APIRouter | None): An optional FastAPI router to use. If None, a new router will be created.

    Returns:
        APIRouter: A FastAPI router with CRUD endpoints.
    """
    if router is None:
        router = APIRouter()
    # model = model_crud.model

    @router.post("/{item_id}/creators/", response_model=schema)
    async def add_creator_with_body(item_id: UUID, creator: ImageCreatorSchema | None, db: Annotated[Session, Depends(get_db)]) -> BaseModel:
        """Add a creator to an image.

        Args:
            item_id (UUID): The ID of the item to which the creator is being added.
            creator (ImageCreatorSchema | None): The creator data to be added.
            db (Session): The database session.

        Raises:
            HTTPException: If the creation fails.

        Returns:
            ImageSchema: The created item.
        """
        return model_crud.add_creator(db=db, crud=image_creator_crud, item_id=item_id, creator=creator)

    @router.post("/{item_id}/creators/{creator_id}", response_model=schema)
    async def add_creator(item_id: UUID, creator_id: UUID, db: Annotated[Session, Depends(get_db)]) -> BaseModel:
        """Add a creator to an image.

        Args:
            item_id (UUID): The ID of the item to which the creator is being added.
            creator_id (UUID): The ID of the creator being added.
            db (Session): The database session.

        Raises:
            HTTPException: If the creation fails.

        Returns:
            ImageSchema: The created item.
        """
        return model_crud.add_creator(db=db, crud=image_creator_crud, item_id=item_id, creator_id=creator_id)

    return router
