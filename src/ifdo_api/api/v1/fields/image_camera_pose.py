# ifdo_api/api/v1/fields/image_camera_pose.py
from fastapi import APIRouter
from ifdo_api.api.generic_router import generate_crud_router
from ifdo_api.crud.fields import image_camera_pose_crud
from ifdo_api.schemas.fields import ImageCameraPoseSchema

router: APIRouter = generate_crud_router(
    model_crud=image_camera_pose_crud,
    schema=ImageCameraPoseSchema,
    schema_create=ImageCameraPoseSchema,
)
