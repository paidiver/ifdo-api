"""This module implements the CRUD for the Image model."""

from sqlalchemy.orm import Session
from ifdo_api.crud.base import CRUDBase
from ifdo_api.crud.base import jsonable_encoder_exclude_none_and_empty
from ifdo_api.crud.dataset import dataset_crud
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
from ifdo_api.models.image import Image
from ifdo_api.schemas.image import ImageSchema

image_models_info = {
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
}


class CRUDImage(CRUDBase[Image]):
    """CRUD object with default methods to Create, Read, Update, Delete (CRUD).

    Args:
        CRUDBase (ModelType): Base class for CRUD operations.
    """

    def create(self, db: Session, *, obj_in: ImageSchema) -> Image:
        """Create a new object in the database.

        Args:
            db (Session): Database session.
            obj_in (ModelType): Object to be created.

        Returns:
            ModelType: The created object.
        """
        obj_in_data = jsonable_encoder_exclude_none_and_empty(obj_in)
        dataset_crud.show(db=db, id_pk=obj_in_data["dataset_id"])

        obj_in_data = self.create_fields(db, obj_in_data, image_models_info)

        db_obj = self.model(**obj_in_data)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


image_crud = CRUDImage(Image)
