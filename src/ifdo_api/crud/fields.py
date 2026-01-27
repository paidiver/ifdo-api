"""This module implements the CRUD for the Fields model."""

from ifdo_api.crud.base import CRUDBase
from ifdo_api.models.fields import PI
from ifdo_api.models.fields import Context
from ifdo_api.models.fields import Creator
from ifdo_api.models.fields import Event
from ifdo_api.models.fields import ImageCameraCalibrationModel
from ifdo_api.models.fields import ImageCameraHousingViewport
from ifdo_api.models.fields import ImageCameraPose
from ifdo_api.models.fields import ImageDomeportParameter
from ifdo_api.models.fields import ImageFlatportParameter
from ifdo_api.models.fields import ImagePhotometricCalibration
from ifdo_api.models.fields import License
from ifdo_api.models.fields import Platform
from ifdo_api.models.fields import Project
from ifdo_api.models.fields import RelatedMaterial
from ifdo_api.models.fields import Sensor


class CRUDImageContext(CRUDBase[Context]):
    """CRUD object with default methods to Create, Read, Update, Delete (CRUD).

    Args:
        CRUDBase (ModelType): Base class for CRUD operations.
    """


class CRUDImageProject(CRUDBase[Project]):
    """CRUD object with default methods to Create, Read, Update, Delete (CRUD).

    Args:
        CRUDBase (ModelType): Base class for CRUD operations.
    """


class CRUDImageEvent(CRUDBase[Event]):
    """CRUD object with default methods to Create, Read, Update, Delete (CRUD).

    Args:
        CRUDBase (ModelType): Base class for CRUD operations.
    """


class CRUDImagePlatform(CRUDBase[Platform]):
    """CRUD object with default methods to Create, Read, Update, Delete (CRUD).

    Args:
        CRUDBase (ModelType): Base class for CRUD operations.
    """


class CRUDImageSensor(CRUDBase[Sensor]):
    """CRUD object with default methods to Create, Read, Update, Delete (CRUD).

    Args:
        CRUDBase (ModelType): Base class for CRUD operations.
    """


class CRUDImagePI(CRUDBase[PI]):
    """CRUD object with default methods to Create, Read, Update, Delete (CRUD).

    Args:
        CRUDBase (ModelType): Base class for CRUD operations.
    """


class CRUDImageCreator(CRUDBase[Creator]):
    """CRUD object with default methods to Create, Read, Update, Delete (CRUD).

    Args:
        CRUDBase (ModelType): Base class for CRUD operations.
    """


class CRUDImageLicense(CRUDBase[License]):
    """CRUD object with default methods to Create, Read, Update, Delete (CRUD).

    Args:
        CRUDBase (ModelType): Base class for CRUD operations.
    """


class CRUDImageCameraPose(CRUDBase[ImageCameraPose]):
    """CRUD object with default methods to Create, Read, Update, Delete (CRUD).

    Args:
        CRUDBase (ModelType): Base class for CRUD operations.
    """


class CRUDImageCameraHousingViewport(CRUDBase[ImageCameraHousingViewport]):
    """CRUD object with default methods to Create, Read, Update, Delete (CRUD).

    Args:
        CRUDBase (ModelType): Base class for CRUD operations.
    """


class CRUDImageFlatportParameter(CRUDBase[ImageFlatportParameter]):
    """CRUD object with default methods to Create, Read, Update, Delete (CRUD).

    Args:
        CRUDBase (ModelType): Base class for CRUD operations.
    """


class CRUDImageDomeportParameter(CRUDBase[ImageDomeportParameter]):
    """CRUD object with default methods to Create, Read, Update, Delete (CRUD).

    Args:
        CRUDBase (ModelType): Base class for CRUD operations.
    """


class CRUDImageCameraCalibrationModel(CRUDBase[ImageCameraCalibrationModel]):
    """CRUD object with default methods to Create, Read, Update, Delete (CRUD).

    Args:
        CRUDBase (ModelType): Base class for CRUD operations.
    """


class CRUDImagePhotometricCalibration(CRUDBase[ImagePhotometricCalibration]):
    """CRUD object with default methods to Create, Read, Update, Delete (CRUD).

    Args:
        CRUDBase (ModelType): Base class for CRUD operations.
    """


class CRUDRelatedMaterial(CRUDBase[RelatedMaterial]):
    """CRUD object with default methods to Create, Read, Update, Delete (CRUD).

    Args:
        CRUDBase (ModelType): Base class for CRUD operations.
    """


context_crud = CRUDImageContext(Context)
project_crud = CRUDImageProject(Project)
event_crud = CRUDImageEvent(Event)
platform_crud = CRUDImagePlatform(Platform)
sensor_crud = CRUDImageSensor(Sensor)
pi_crud = CRUDImagePI(PI)
creator_crud = CRUDImageCreator(Creator)
license_crud = CRUDImageLicense(License)
image_camera_pose_crud = CRUDImageCameraPose(ImageCameraPose)
image_camera_housing_viewport_crud = CRUDImageCameraHousingViewport(ImageCameraHousingViewport)
image_flatport_parameter_crud = CRUDImageFlatportParameter(ImageFlatportParameter)
image_domeport_parameter_crud = CRUDImageDomeportParameter(ImageDomeportParameter)
image_camera_calibration_model_crud = CRUDImageCameraCalibrationModel(ImageCameraCalibrationModel)
image_photometric_calibration_crud = CRUDImagePhotometricCalibration(ImagePhotometricCalibration)
related_material_crud = CRUDRelatedMaterial(RelatedMaterial)
