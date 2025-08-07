"""Base class for CRUD operations."""

import datetime
from decimal import Decimal
from typing import Any
from typing import Generic
from typing import TypeVar
from uuid import UUID
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import HttpUrl
from sqlalchemy import desc
from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from ifdo_api.api.exceptions import NotFoundException
from ifdo_api.api.exceptions import ValueErrorException
from ifdo_api.models.base import Base
from ifdo_api.models.fields import ImageCreator
from ifdo_api.models.image import Image
from ifdo_api.schemas.fields import ImageCreatorSchema

ModelType = TypeVar("ModelType", bound=Base)  # type: ignore[name-defined]


class CRUDBase(Generic[ModelType]):
    """CRUD object with default methods to Create, Read, Update, Delete (CRUD).

    Args:
        ModelType (Base): Base class for CRUD operations.
    """

    def __init__(self, model: ModelType):
        self.model = model

    def show(self, db: Session, id_pk: int | None = None, uuid: UUID | None = None) -> ModelType | None:
        """Retrieve an object from the database by its primary key.

        Args:
            db (Session): Database session.
            id_pk (int | None): Primary key of the object to retrieve.
            uuid (UUID | None): UUID of the object to retrieve.

        Returns:
            ModelType | None: The object if found, otherwise None.
        """
        if id_pk is None and uuid is None:
            detail = "Either id_pk or uuid must be provided"
            raise ValueErrorException(detail)
        db_item = None
        if uuid is not None:
            db_item = db.query(self.model).filter(self.model.uuid == uuid).one_or_none()
        else:
            db_item = db.query(self.model).filter(self.model.id == id_pk).one_or_none()
        if not db_item:
            raise NotFoundException(self.model.__name__)
        return db_item

    def index(
        self, db: Session, *, limit: int | None = None, arguments: dict | None = None, order_by: str = "created_at", desc_order: bool = True
    ) -> list[ModelType]:
        """Retrieve a list of objects from the database.

        Args:
            db (Session): Database session.
            limit (int | None): Maximum number of results to return.
            arguments (dict | None): Filter arguments for the query.
            order_by (str): Column name to order the results by.
            desc_order (bool): Whether to order the results in descending order.

        Returns:
            list[ModelType]: List of objects from the database.
        """
        query = self.create_query(arguments) if arguments else "true"

        column_attr = getattr(self.model, order_by, None)
        if column_attr is None:
            detail = f"Invalid order_by column: {order_by}"
            raise ValueErrorException(detail)
        order_clause = desc(column_attr) if desc_order else column_attr

        if limit:
            result = db.query(self.model).filter(text(query)).limit(limit).order_by(order_clause).all()
        else:
            result = db.query(self.model).filter(text(query)).order_by(order_clause).all()

        return result

    def create(self, db: Session, *, obj_in: ModelType | dict) -> ModelType:
        """Create a new object in the database.

        Args:
            db (Session): Database session.
            obj_in (ModelType | dict): Object to be created.

        Returns:
            ModelType: The created object.
        """
        if not isinstance(obj_in, dict):
            obj_in = jsonable_encoder_exclude_none_and_empty(obj_in)

        db_obj = self.model(**obj_in)

        max_id = db.query(func.max(self.model.id)).first()

        if max_id[0]:
            db_obj.id = max_id[0] + 1
        else:
            db_obj.id = 1

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, *, id_pk: int | None = None, uuid: UUID | None = None, obj_in: ModelType | dict[str, Any]) -> ModelType:
        """Update an existing object in the database.

        Args:
            db (Session): Database session.
            id_pk (int | None): Primary key of the object to be updated.
            uuid (UUID | None): UUID of the object to be updated.
            obj_in (ModelType | dict[str, Any]): Object data to update.

        Returns:
            ModelType: The updated object.
        """
        if id_pk is None and uuid is None:
            detail = "Either id_pk or uuid must be provided"
            raise ValueErrorException(detail)

        if uuid is not None:
            obj_old = db.query(self.model).filter(self.model.uuid == uuid)
        else:
            obj_old = db.query(self.model).filter(self.model.id == id_pk).first()
        if not obj_old:
            raise NotFoundException(self.model.__name__)
        update_data = obj_in if isinstance(obj_in, dict) else obj_in.dict(exclude_unset=True)
        update_data = convert_pydantic_types(update_data)

        for field in vars(obj_old):
            if field in update_data:
                setattr(obj_old, field, update_data[field])

        db.add(obj_old)
        db.commit()
        db.refresh(obj_old)
        return obj_old

    def delete(self, db: Session, *, id_pk: int | None = None, uuid: UUID | None = None) -> ModelType:
        """Delete an object from the database.

        Args:
            db (Session): Database session.
            id_pk (int | None): Primary key of the object to be deleted.
            uuid (UUID | None): UUID of the object to be deleted.

        Returns:
            ModelType: The deleted object.
        """
        obj = db.query(self.model).filter(self.model.uuid == uuid) if uuid is not None else db.query(self.model).get(id_pk)
        obj = obj.one_or_none() if obj else None
        if not obj:
            raise NotFoundException(self.model.__name__)
        db.delete(obj)
        db.commit()
        return obj

    def create_query(self, kwargs: dict) -> str:
        """Create a SQL query string based on the provided keyword arguments.

        Args:
            kwargs (dict): Keyword arguments representing the query conditions.

        Returns:
            str: The constructed SQL query string.
        """
        x = 0
        query = ""
        for key, value in kwargs.items():
            beginning = "" if x == 0 else " AND"
            if isinstance(value, list):
                if len(value[1]) == 1:
                    query += f"{beginning} {key} {value[0]} ('{value[1][0]}')"
                else:
                    query += f"{beginning} {key} {value[0]} {tuple(value[1])}"
            else:
                query += f"{beginning} {key} '{value}'"
            x = 1

        return query

    def create_fields(self, db: Session, model_dict: dict, models_info: dict) -> dict:
        """Create fields for the dataset.

        Args:
            db (Session): Database session.
            model_dict (dict): The dataset dictionary to update.
            models_info (dict): Dictionary containing the CRUD and schema information for each field.

        Returns:
            dict: Updated dataset dictionary with fields created.
        """
        for key, value in models_info.items():
            if key in model_dict:
                new_value = model_dict[key]
                data_type = list if value.get("list") else dict
                if new_value and isinstance(new_value, data_type):
                    if data_type is list:
                        items = []
                        for item in new_value:
                            new_item = self.get_or_create(db, value["crud"], value.get("unique"), item)
                            items.append(new_item)
                        model_dict[key] = items
                    else:
                        new_item = self.get_or_create(db, value["crud"], value.get("unique"), new_value)
                        model_dict[key] = new_item
                        if f"{key}_id" in model_dict:
                            del model_dict[f"{key}_id"]

        return model_dict

    def add_creator(
        self, db: Session, crud: ModelType, item_id: UUID, creator_id: UUID | None = None, creator: ImageCreatorSchema | None = None
    ) -> Image:
        """Add a creator to an image.

        Args:
            db (Session): Database session.
            crud (ModelType): The CRUD object for image creators.
            item_id (UUID): The ID of the image.
            creator_id (UUID): The ID of the creator to add.
            creator (ImageCreatorSchema): The creator object to add.

        Returns:
            ModelType: The updated model with the new creator.
        """
        if not creator_id and not creator:
            msg = "Either creator_id or creator must be provided."
            raise ValueErrorException(msg)
        if creator_id and creator:
            msg = "Only one of creator_id or creator should be provided."
            raise ValueErrorException(msg)
        if creator:
            creator = jsonable_encoder_exclude_none_and_empty(creator)
            db_creator = self.get_or_create(db, crud, "name", creator)
        else:
            db_creator = crud.show(db, uuid=creator_id)
        if not db_creator:
            raise NotFoundException(ImageCreator.__name__)
        db_item = self.show(db=db, uuid=item_id)
        if not db_item:
            raise NotFoundException(self.model.__name__)
        if db_creator in db_item.creators:
            msg = "Creator already exists in the image."
            raise ValueErrorException(msg)
        db_item.creators.append(db_creator)
        db.commit()
        db.refresh(db_item)
        return db_item

    def get_or_create(self, db: Session, crud: ModelType, unique: str | None, data: dict[str, any]) -> ModelType | None:
        """Helper to get or create an object in the database.

        Args:
            db (Session): Database session.
            crud (ModelType): The CRUD object to use for the operation.
            unique (str | None): Unique field to check for existing objects.
            data (dict[str, any]): Data to be used for creating or finding the object.

        Returns:
            ModelType | None: The found or created object.
        """
        instance = None
        model = crud.model
        if unique:
            instance = db.query(model).filter(getattr(model, unique) == data.get(unique)).first()
        if not instance:
            instance = model(**data)
            db.add(instance)
            db.flush()
        return instance


def convert_pydantic_types(data: dict[str, Any]) -> dict[str, Any]:
    """Convert Pydantic-specific types to native Python types.

    Args:
        data (dict[str, Any]): Dictionary containing Pydantic types.

    Returns:
        dict[str, Any]: Dictionary with Pydantic types converted to native Python types.
    """
    converted = {}
    for key, value in data.items():
        if isinstance(value, (HttpUrl, EmailStr)):
            converted[key] = str(value)
        elif isinstance(value, Decimal):
            converted[key] = float(value)
        elif isinstance(value, datetime.datetime):
            converted[key] = value  # SQLAlchemy supports native datetime
        elif isinstance(value, BaseModel):
            converted[key] = convert_pydantic_types(value.dict())
        else:
            converted[key] = value
    return converted


def jsonable_encoder_exclude_none_and_empty(obj: BaseModel) -> dict[str, Any]:
    """Convert a Pydantic model to a JSON-serializable dictionary, excluding None and empty values.

    Args:
        obj (BaseModel): The Pydantic model to convert.

    Returns:
        dict[str, Any]: A dictionary representation of the model with None and empty values excluded.
    """
    data = jsonable_encoder(obj, exclude_none=True)
    return {k: v for k, v in data.items() if v != []}
