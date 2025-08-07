"""This module implements the CRUD for the Fields model."""

from ifdo_api.crud.base import CRUDBase
from ifdo_api.models.fields import ImageCameraCalibrationModel
from ifdo_api.models.fields import ImageCameraHousingViewport
from ifdo_api.models.fields import ImageCameraPose
from ifdo_api.models.fields import ImageContext
from ifdo_api.models.fields import ImageCreator
from ifdo_api.models.fields import ImageDomeportParameter
from ifdo_api.models.fields import ImageEvent
from ifdo_api.models.fields import ImageFlatportParameter
from ifdo_api.models.fields import ImageLicense
from ifdo_api.models.fields import ImagePhotometricCalibration
from ifdo_api.models.fields import ImagePI
from ifdo_api.models.fields import ImagePlatform
from ifdo_api.models.fields import ImageProject
from ifdo_api.models.fields import ImageSensor
from ifdo_api.models.fields import ImageSetRelatedMaterial


class CRUDImageContext(CRUDBase[ImageContext]):
    """CRUD object with default methods to Create, Read, Update, Delete (CRUD).

    Args:
        CRUDBase (ModelType): Base class for CRUD operations.
    """


class CRUDImageProject(CRUDBase[ImageProject]):
    """CRUD object with default methods to Create, Read, Update, Delete (CRUD).

    Args:
        CRUDBase (ModelType): Base class for CRUD operations.
    """


class CRUDImageEvent(CRUDBase[ImageEvent]):
    """CRUD object with default methods to Create, Read, Update, Delete (CRUD).

    Args:
        CRUDBase (ModelType): Base class for CRUD operations.
    """


class CRUDImagePlatform(CRUDBase[ImagePlatform]):
    """CRUD object with default methods to Create, Read, Update, Delete (CRUD).

    Args:
        CRUDBase (ModelType): Base class for CRUD operations.
    """


class CRUDImageSensor(CRUDBase[ImageSensor]):
    """CRUD object with default methods to Create, Read, Update, Delete (CRUD).

    Args:
        CRUDBase (ModelType): Base class for CRUD operations.
    """


class CRUDImagePI(CRUDBase[ImagePI]):
    """CRUD object with default methods to Create, Read, Update, Delete (CRUD).

    Args:
        CRUDBase (ModelType): Base class for CRUD operations.
    """


class CRUDImageCreator(CRUDBase[ImageCreator]):
    """CRUD object with default methods to Create, Read, Update, Delete (CRUD).

    Args:
        CRUDBase (ModelType): Base class for CRUD operations.
    """


class CRUDImageLicense(CRUDBase[ImageLicense]):
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


class CRUDImageSetRelatedMaterial(CRUDBase[ImageSetRelatedMaterial]):
    """CRUD object with default methods to Create, Read, Update, Delete (CRUD).

    Args:
        CRUDBase (ModelType): Base class for CRUD operations.
    """


image_context_crud = CRUDImageContext(ImageContext)
image_project_crud = CRUDImageProject(ImageProject)
image_event_crud = CRUDImageEvent(ImageEvent)
image_platform_crud = CRUDImagePlatform(ImagePlatform)
image_sensor_crud = CRUDImageSensor(ImageSensor)
image_pi_crud = CRUDImagePI(ImagePI)
image_creator_crud = CRUDImageCreator(ImageCreator)
image_license_crud = CRUDImageLicense(ImageLicense)
image_camera_pose_crud = CRUDImageCameraPose(ImageCameraPose)
image_camera_housing_viewport_crud = CRUDImageCameraHousingViewport(ImageCameraHousingViewport)
image_flatport_parameter_crud = CRUDImageFlatportParameter(ImageFlatportParameter)
image_domeport_parameter_crud = CRUDImageDomeportParameter(ImageDomeportParameter)
image_camera_calibration_model_crud = CRUDImageCameraCalibrationModel(ImageCameraCalibrationModel)
image_photometric_calibration_crud = CRUDImagePhotometricCalibration(ImagePhotometricCalibration)
image_set_related_material_crud = CRUDImageSetRelatedMaterial(ImageSetRelatedMaterial)
