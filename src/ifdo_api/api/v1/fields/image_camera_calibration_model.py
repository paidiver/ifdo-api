# ifdo_api/api/v1/fields/image_camera_calibration_model.py
from fastapi import APIRouter
from ifdo_api.api.generic_router import generate_crud_router
from ifdo_api.crud.fields import image_camera_calibration_model_crud
from ifdo_api.schemas.fields import ImageCameraCalibrationModelSchema

router: APIRouter = generate_crud_router(
    model_crud=image_camera_calibration_model_crud,
    schema=ImageCameraCalibrationModelSchema,
    schema_create=ImageCameraCalibrationModelSchema,
)
