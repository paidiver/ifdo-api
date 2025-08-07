"""This module implements the CRUD for the Dataset model."""

from uuid import UUID
from sqlalchemy import func
from sqlalchemy.orm import Session
from ifdo_api.api.exceptions import NotFoundException
from ifdo_api.api.exceptions import ValueErrorException
from ifdo_api.crud.annotation import annotator_crud
from ifdo_api.crud.annotation import label_crud
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
from ifdo_api.schemas.annotation import AnnotatorSchema
from ifdo_api.schemas.annotation import LabelSchema
from ifdo_api.schemas.dataset import DatasetSchema
from ifdo_api.schemas.ifdo import ifdo_common_relationship_mapping
from ifdo_api.schemas.ifdo import ifdo_header_relational_mapping
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

        max_id = db.query(func.max(self.model.id)).first()

        if max_id[0]:
            db_obj.id = max_id[0] + 1
        else:
            db_obj.id = 1

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def add_image(self, db: Session, crud: ModelType, item_id: UUID, image_id: UUID | None = None, image: ImageSchema | None = None) -> Image:
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
            db_image = crud.show(db, uuid=image_id)
        if not db_image:
            raise NotFoundException(Image.__name__)
        db_item = self.show(db=db, uuid=item_id)
        if not db_item:
            raise NotFoundException(self.model.__name__)
        if db_image in db_item.images:
            msg = "Image already exists in the dataset."
            raise ValueErrorException(msg)
        db_item.images.append(db_image)
        db.commit()
        db.refresh(db_item)
        return db_item

    # def create_from_ifdo(self, db: Session, ifdo_data: dict) -> Dataset:
    #     """Create a dataset from IFDO data.

    #     Args:
    #         db (Session): Database session.
    #         ifdo_data (dict): IFDO data to create the dataset.

    #     Returns:
    #         Dataset: The created dataset.
    #     """
    #     image_set_header = ifdo_data.get("image-set-header")
    #     if not image_set_header:
    #         msg = "Image set header is required in IFDO data"
    #         raise ValueErrorException(msg)
    #     dataset = self.create_dataset_from_header(
    #         db=db,
    #         image_set_header=image_set_header,
    #     )

    #     image_set_items = ifdo_data.get("image-set-items")
    #     if not image_set_items:
    #         msg = "Image set items is required in IFDO data"
    #         raise ValueErrorException(msg)
    #     self.create_images_from_set_items(
    #         db=db,
    #         image_set_items=image_set_items,
    #         dataset=dataset,
    #     )
    #     return dataset

    # def create_images_from_set_items(
    #     self,
    #     db: Session,
    #     image_set_items: dict[str, dict],
    #     dataset: Dataset,
    # ) -> list[Image]:
    #     """Create images from the image set items.

    #     Args:
    #         db (Session): Database session.
    #         image_set_items (dict[str, dict]): The image set items containing image information.
    #         dataset (Dataset): The dataset to which the images belong.

    #     Returns:
    #         list[Image]: The list of created images.
    #     """
    #     return []
    #     # for item_name, item_data in image_set_items.items():
    #     #     image_dict = {}
    #     #     image_dict["dataset_id"] = dataset.id
    #     #     image_dict["name"] = item_name
    #     #     image_dict = self.create_common_fields(
    #     #         db=db,
    #     #         dataset_dict=image_dict,
    #     #         item_data=item_data,
    #     #     )
    #     #     image_dict = self.create_annotations(
    #     #         db=db,
    #     #         dataset_dict=image_dict,
    #     #         item_data=item_data,
    #     #     )
    #     #     new_image = ImageSchema(**image_dict)
    #     #     db.add(new_image)
    #     #     db.commit()
    #     #     db.refresh(new_image)
    #     #     images.append(new_image)

    # def create_dataset_from_header(
    #     self,
    #     db: Session,
    #     image_set_header: dict,
    # ) -> Dataset:
    #     """Create a dataset from the image set header.

    #     Args:
    #         db (Session): Database session.
    #         image_set_header (dict): The image set header containing dataset information.

    #     Returns:
    #         Dataset: The created dataset.
    #     """
    #     dataset_dict = {}
    #     for key, value in ifdo_header_mapping.items():
    #         if key in image_set_header:
    #             dataset_dict[value] = image_set_header[key]
    #     for key, value in ifdo_common_mapping.items():
    #         if key in image_set_header:
    #             dataset_dict[value] = image_set_header[key]
    #     dataset_dict = self.create_common_fields(
    #         db=db,
    #         dataset_dict=dataset_dict,
    #         image_set_header=image_set_header,
    #     )
    #     dataset_dict = self.create_annotations(
    #         db=db,
    #         dataset_dict=dataset_dict,
    #         image_set_header=image_set_header,
    #     )
    #     new_dataset = DatasetSchema(**dataset_dict)
    #     db.add(new_dataset)
    #     db.commit()
    #     db.refresh(new_dataset)
    #     return new_dataset

    def create_common_fields(
        self,
        db: Session,
        dataset_dict: dict,
        image_set_header: dict,
    ) -> dict:
        """Create common fields for the dataset.

        Args:
            db (Session): Database session.
            dataset_dict (dict): The dataset dictionary to update.
            image_set_header (dict): The image set header containing common fields.

        Returns:
            dict: Updated dataset dictionary with common fields.
        """
        for key, value in ifdo_common_relationship_mapping.items():
            if key in image_set_header:
                new_value = image_set_header[key]
                schema = value["schema"]
                if isinstance(new_value, list):
                    new_item = [value["crud"].create(db=db, obj_in=schema(item)) for item in new_value]
                    dataset_dict[value["field_name"]] = [item.id for item in new_item]
                else:
                    new_item = value["crud"].create(db=db, obj_in=schema(new_value))
                    dataset_dict[value["field_name"]] = new_item.id
        for key, value in ifdo_header_relational_mapping.items():
            if key in image_set_header:
                new_value = image_set_header[key]
                new_item = value["crud"].create(db=db, obj_in=schema(new_value))
                dataset_dict[value["field_name"]] = new_item.id
        return dataset_dict

    def create_annotations(
        self,
        db: Session,
        dataset_dict: dict,
        image_set_header: dict,
    ) -> dict:
        """Create annotations for the dataset.

        Args:
            db (Session): Database session.
            dataset_dict (dict): The dataset dictionary to update.
            image_set_header (dict): The image set header containing annotations.

        Returns:
            dict: Updated dataset dictionary with annotations.
        """
        annotations = {}
        if "image-annotation-label" in image_set_header:
            annotations["label"] = image_set_header.get("image-annotation-labels", [])
            dataset_dict["annotation_labels"] = []
            for label in annotations["label"]:
                label_schema = {}
                if "name" in label:
                    label_schema["name"] = label["name"]
                if "info" in label:
                    label_schema["info"] = label["info"]
                if "id" in label and "uuid" not in label:
                    label_schema["uuid"] = label["uuid"]
                obj_in = LabelSchema(**label_schema)
                new_label = label_crud.create(db=db, obj_in=obj_in)
                dataset_dict["annotation_labels"].append(new_label.id)
            annotations["annotators"] = image_set_header.get("image-annotation-creators", [])
            dataset_dict["annotation_creators"] = []
            for annotator in annotations["annotators"]:
                annotator_schema = {}
                if "name" in annotator:
                    annotator_schema["name"] = annotator["name"]
                if "id" in annotator and "uuid" not in annotator:
                    annotator_schema["uuid"] = annotator["uuid"]
                obj_in = AnnotatorSchema(**annotator_schema)
                new_annotator = annotator_crud.create(db=db, obj_in=obj_in)
                dataset_dict["annotation_creators"].append(new_annotator.id)
                # annotator["id"] = new_annotator.id
        return dataset_dict

    # def create_provenance(
    #     self,
    #     db: Session,
    #     dataset_dict: dict,
    #     provenance_obj: dict,
    # ) -> dict:
    #     """Create provenance information for the dataset.

    #     Args:
    #         db (Session): Database session.
    #         dataset_dict (dict): The dataset dictionary to update.
    #         provenance_obj (dict): The provenance object containing agents, entities, and activities.

    #     Returns:
    #         dict: Updated dataset dictionary with provenance information.
    #     """
    #     if "image-set-provenance" in image_set_header:
    #         provenance_agents = provenance_obj.get("provenance-agents", [])
    #         provenance_entities = provenance_obj.get("provenance-entities", [])
    #         provenance_activities = provenance_obj.get("provenance-activities", [])
    #         if provenance_agents:
    #             for agent in provenance_agents:
    #                 obj_in = ProvenanceAgentSchema(
    #                     name=agent["name"],
    #                     unique_id=agent["id"]
    #                 )
    #                 new_agent = provenance_agent_crud.create(
    #                     db=db, obj_in=obj_in
    #                 )

    #             new_item = value["crud"].create(db=db, obj_in=value["schema"](new_value))
    #             dataset_dict[value["field_name"]] = new_item.id

    #         for key, value in ifdo_provenance_mapping.items():
    #             if key in image_set_header["image-set-provenance"]:
    #                 new_value = image_set_header["image-set-provenance"][key]
    #                 if isinstance(new_value, list):
    #                     new_item = [value["crud"].create(db=db, obj_in=value["schema"](item)) for item in new_value]
    #                     dataset_dict[value["field_name"]] = [item.id for item in new_item]
    #                 else:
    #                     new_item = value["crud"].create(db=db, obj_in=value["schema"](new_value))
    #                     dataset_dict[value["field_name"]] = new_item.id

    #         for key, value in ifdo_provenance_mapping.items():
    #             if key in image_set_header:
    #                 new_value = image_set_header[key]
    #                 if isinstance(new_value, list):
    #                     new_item = [value["crud"].create(db=db, obj_in=value["schema"](item)) for item in new_value]
    #                     dataset_dict[value["field_name"]] = [item.id for item in new_item]
    #                 else:
    #                     new_item = value["crud"].create(db=db, obj_in=value["schema"](new_value))
    #                     dataset_dict[value["field_name"]] = new_item.id
    #     return dataset_dict


dataset_crud = CRUDDataset(Dataset)
