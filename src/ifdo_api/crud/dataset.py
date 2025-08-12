"""This module implements the CRUD for the Dataset model."""

from uuid import UUID
from sqlalchemy import desc
from sqlalchemy.orm import Session
from sqlalchemy.orm import noload
from sqlalchemy.orm import selectinload
from sqlalchemy.sql import text
from ifdo_api.api.exceptions import NotFoundException
from ifdo_api.api.exceptions import ValueErrorException
from ifdo_api.crud.base import CRUDBase
from ifdo_api.crud.base import ModelType
from ifdo_api.crud.base import jsonable_encoder_exclude_none_and_empty
from ifdo_api.crud.fields import image_camera_calibration_model_crud
from ifdo_api.crud.fields import image_camera_housing_viewport_crud
from ifdo_api.crud.fields import image_camera_pose_crud
from ifdo_api.crud.fields import image_context_crud
from ifdo_api.crud.fields import image_creator_crud
from ifdo_api.crud.fields import image_domeport_parameter_crud
from ifdo_api.crud.fields import image_event_crud
from ifdo_api.crud.fields import image_flatport_parameter_crud
from ifdo_api.crud.fields import image_license_crud
from ifdo_api.crud.fields import image_photometric_calibration_crud
from ifdo_api.crud.fields import image_pi_crud
from ifdo_api.crud.fields import image_platform_crud
from ifdo_api.crud.fields import image_project_crud
from ifdo_api.crud.fields import image_sensor_crud
from ifdo_api.crud.fields import image_set_related_material_crud
from ifdo_api.models.dataset import Dataset
from ifdo_api.models.image import Image
from ifdo_api.schemas.dataset import DatasetSchema
from ifdo_api.schemas.ifdo import ifdo_mapping
from ifdo_api.schemas.image import ImageSchema

# from ifdo_api.crud.provenance import provenance_agent_crud
# from ifdo_api.schemas.ifdo import ifdo_provenance_mapping
# from ifdo_api.schemas.provenance import ProvenanceAgentSchema


dataset_models_info = {
    "context": {"crud": image_context_crud, "unique": "name"},
    "project": {"crud": image_project_crud, "unique": "name"},
    "event": {"crud": image_event_crud, "unique": "name"},
    "platform": {"crud": image_platform_crud, "unique": "name"},
    "sensor": {"crud": image_sensor_crud, "unique": "name"},
    "pi": {"crud": image_pi_crud, "unique": "name"},
    "license": {"crud": image_license_crud, "unique": "name"},
    "camera_pose": {
        "crud": image_camera_pose_crud,
    },
    "camera_housing_viewport": {
        "crud": image_camera_housing_viewport_crud,
    },
    "flatport_parameter": {
        "crud": image_flatport_parameter_crud,
    },
    "domeport_parameter": {
        "crud": image_domeport_parameter_crud,
    },
    "camera_calibration_model": {
        "crud": image_camera_calibration_model_crud,
    },
    "photometric_calibration": {
        "crud": image_photometric_calibration_crud,
    },
    "creators": {"crud": image_creator_crud, "list": True, "unique": "name"},
    "related_materials": {
        "crud": image_set_related_material_crud,
        "list": True,
    },
}


class CRUDDataset(CRUDBase[Dataset]):
    """CRUD object with default methods to Create, Read, Update, Delete (CRUD).

    Args:
        CRUDBase (ModelType): Base class for CRUD operations.
    """

    def show(self, db: Session, id_pk: int, include_images: bool = False) -> ModelType | None:
        """Retrieve an object from the database by its primary key.

        Args:
            db (Session): Database session.
            id_pk (UUID): Primary key of the object to retrieve.
            include_images (bool): Whether to include images in the result. Defaults to False.

        Returns:
            ModelType | None: The object if found, otherwise None.
        """
        query = db.query(self.model).filter(self.model.id == id_pk)
        query = query.options(selectinload(self.model.images)) if include_images else query.options(noload(self.model.images))
        db_item = query.one_or_none()
        if not db_item:
            raise NotFoundException(self.model.__name__)
        return db_item

    def index(
        self,
        db: Session,
        *,
        limit: int | None = None,
        arguments: dict | None = None,
        order_by: str = "created_at",
        desc_order: bool = True,
        include_images: bool = False,
    ) -> list[ModelType]:
        """Retrieve a list of objects from the database.

        Args:
            db (Session): Database session.
            limit (int | None): Maximum number of results to return.
            arguments (dict | None): Filter arguments for the query.
            order_by (str): Column name to order the results by.
            desc_order (bool): Whether to order the results in descending order.
            include_images (bool): Whether to include images in the results.

        Returns:
            list[ModelType]: List of objects from the database.
        """
        query_str = self.create_query(arguments) if arguments else "true"

        column_attr = getattr(self.model, order_by, None)
        if column_attr is None:
            detail = f"Invalid order_by column: {order_by}"
            raise ValueErrorException(detail)
        order_clause = desc(column_attr) if desc_order else column_attr

        query = db.query(self.model).filter(text(query_str))

        query = query.options(selectinload(self.model.images)) if include_images else query.options(noload(self.model.images))
        if limit:
            query = query.limit(limit)

        return query.order_by(order_clause).all()

    def create(self, db: Session, *, obj_in: DatasetSchema) -> Dataset:
        """Create a new object in the database.

        Args:
            db (Session): Database session.
            obj_in (ModelType): Object to be created.

        Returns:
            ModelType: The created object.
        """
        obj_in_data = jsonable_encoder_exclude_none_and_empty(obj_in)
        obj_in_data = self.create_fields(db, obj_in_data, dataset_models_info)

        db_obj = self.model(**obj_in_data)
        db.add(db_obj)

        try:
            db.commit()
            db.refresh(db_obj)
        except Exception as error:
            db.rollback()  # Undo partial transaction
            msg = "Failed to create the dataset from ifdo data."
            msg += f" Error: {error!s}"
            raise ValueErrorException(msg) from error

        return db_obj

    def add_image(
        self,
        db: Session,
        crud: ModelType,
        item_id: UUID,
        image_id: UUID | None = None,
        image: ImageSchema | None = None,
    ) -> Image:
        """Add a image to a dataset.

        Args:
            db (Session): Database session.
            crud (ModelType): The CRUD object for image.
            item_id (UUID): The ID of the dataset.
            image_id (UUID): The ID of the image to add.
            image (ImageSchema): The image object to add.

        Returns:
            Image: The updated image with the new image.
        """
        if not image_id and not image:
            msg = "Either image_id or image must be provided."
            raise ValueErrorException(msg)
        if image_id and image:
            msg = "Only one of image_id or image should be provided."
            raise ValueErrorException(msg)
        if image:
            image = jsonable_encoder_exclude_none_and_empty(image)
            db_image = self.get_or_create(db, crud, "name", image)
        else:
            db_image = crud.show(db, id_pk=image_id)
        if not db_image:
            raise NotFoundException(Image.__name__)
        db_item = self.show(db=db, id_pk=item_id)
        if not db_item:
            raise NotFoundException(self.model.__name__)
        if db_image in db_item.images:
            msg = "Image already exists in the dataset."
            raise ValueErrorException(msg)
        db_item.images.append(db_image)
        db.commit()
        db.refresh(db_item)
        return db_item

    def create_from_ifdo(self, db: Session, ifdo_data: dict) -> Dataset:
        """Create a dataset from IFDO data.

        Args:
            db (Session): Database session.
            ifdo_data (dict): IFDO data to create the dataset.

        Returns:
            Dataset: The created dataset.
        """
        image_set_header = ifdo_data.get("image-set-header")
        image_set_items = ifdo_data.get("image-set-items")
        if not image_set_header or not image_set_items:
            msg = "Image set header and image set items are required in IFDO data"
            raise ValueErrorException(msg)
        dataset_dict = self.parse_ifdo(db=db, section=image_set_header, section_name="header")
        images = self.parse_ifdo_images(db=db, section=image_set_items)
        dataset_dict["images"] = images

        db_obj = self.model(**dataset_dict)
        db.add(db_obj)

        try:
            db.commit()
            db.refresh(db_obj)
        except Exception as error:
            db.rollback()  # Undo partial transaction
            msg = "Failed to create the dataset from ifdo data."
            msg += f" Error: {error!s}"
            raise ValueErrorException(msg) from error

        return db_obj

    def parse_ifdo_images(
        self,
        db: Session,
        section: dict,
    ) -> list[Image]:
        """Parse IFDO images from the given section.

        Args:
            db (Session): Database session.
            section (dict): The section of the IFDO data containing images.

        Returns:
            list[Image]: A list of Image objects created from the section.
        """
        images = []
        for key, value in section.items():
            value["image-set-name"] = key
            image = self.parse_ifdo(db=db, section=value, section_name="items")
            new_image = Image(**image)

            # db_image = self.get_or_create(db, image_crud, "name", image)
            # new_image = Image(**db_image)
            images.append(new_image)
        return images

    def parse_ifdo(
        self,
        db: Session,
        section: dict,
        section_name: str = "header",
    ) -> dict:
        """Create a dataset from the image set header.

        Args:
            db (Session): Database session.
            section (dict): The section of the ifdo data to parse.
            section_name (str): The name of the section being parsed, defaults to "header".

        Returns:
            dict: The dataset dictionary containing parsed data from the section.
        """
        model_dict = {}
        for key, value in ifdo_mapping.items():
            if key in section:
                location = value.get("location")
                crud = value.get("crud")
                if location is None or location == section_name:
                    if crud:
                        new_value = section[key]
                        data_type = list if value.get("list") else dict
                        if new_value and isinstance(new_value, data_type):
                            if data_type is list:
                                new_item = []
                                for item in new_value:
                                    local_item = self.get_or_create(db, crud, value.get("unique"), item)
                                    new_item.append(local_item)
                            else:
                                new_item = self.get_or_create(db, crud, value.get("unique"), new_value)
                            model_dict[value["field_name"]] = new_item
                    else:
                        new_value = section[key]
                        if value.get("normalize"):
                            new_value = value["normalize"](new_value).value
                        model_dict[value["field_name"]] = new_value
        return model_dict

    # def create_annotations(
    #     self,
    #     db: Session,
    #     dataset_dict: dict,
    #     image_set_header: dict,
    # ) -> dict:
    #     """Create annotations for the dataset.

    #     Args:
    #         db (Session): Database session.
    #         dataset_dict (dict): The dataset dictionary to update.
    #         image_set_header (dict): The image set header containing annotations.

    #     Returns:
    #         dict: Updated dataset dictionary with annotations.
    #     """
    #     annotations = {}
    #     if "image-annotation-label" in image_set_header:
    #         annotations["label"] = image_set_header.get("image-annotation-labels", [])
    #         dataset_dict["annotation_labels"] = []
    #         for label in annotations["label"]:
    #             label_schema = {}
    #             if "name" in label:
    #                 label_schema["name"] = label["name"]
    #             if "info" in label:
    #                 label_schema["info"] = label["info"]
    #             label_schema["uuid"] = label["uuid"]
    #             obj_in = LabelSchema(**label_schema)
    #             new_label = label_crud.create(db=db, obj_in=obj_in)
    #             dataset_dict["annotation_labels"].append(new_label.id)
    #         annotations["annotators"] = image_set_header.get("image-annotation-creators", [])
    #         dataset_dict["annotation_creators"] = []
    #         for annotator in annotations["annotators"]:
    #             annotator_schema = {}
    #             if "name" in annotator:
    #                 annotator_schema["name"] = annotator["name"]
    #             annotator_schema["uuid"] = annotator["uuid"]
    #             obj_in = AnnotatorSchema(**annotator_schema)
    #             new_annotator = annotator_crud.create(db=db, obj_in=obj_in)
    #             dataset_dict["annotation_creators"].append(new_annotator.id)
    #             # annotator["id"] = new_annotator.id
    #     return dataset_dict


dataset_crud = CRUDDataset(Dataset)
