# ifdo_api/api/v1/fields/image_photometric_calibration.py
from fastapi import APIRouter
from ifdo_api.api.generic_router import generate_crud_router
from ifdo_api.crud.fields import image_photometric_calibration_crud
from ifdo_api.schemas.fields import ImagePhotometricCalibrationSchema

router: APIRouter = generate_crud_router(
    model_crud=image_photometric_calibration_crud,
    schema=ImagePhotometricCalibrationSchema,
    schema_create=ImagePhotometricCalibrationSchema,
)
