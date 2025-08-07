from uuid import uuid4
from pydantic import BaseModel
from pydantic import Field
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
from ifdo_api.schemas.dataset import DatasetSchema
from ifdo_api.schemas.fields import ImageCameraCalibrationModelSchema
from ifdo_api.schemas.fields import ImageCameraHousingViewportSchema
from ifdo_api.schemas.fields import ImageCameraPoseSchema
from ifdo_api.schemas.fields import ImageContextSchema
from ifdo_api.schemas.fields import ImageCreatorSchema
from ifdo_api.schemas.fields import ImageDomeportParameterSchema
from ifdo_api.schemas.fields import ImageEventSchema
from ifdo_api.schemas.fields import ImageFlatportParameterSchema
from ifdo_api.schemas.fields import ImageLicenseSchema
from ifdo_api.schemas.fields import ImagePhotometricCalibrationSchema
from ifdo_api.schemas.fields import ImagePISchema
from ifdo_api.schemas.fields import ImagePlatformSchema
from ifdo_api.schemas.fields import ImageProjectSchema
from ifdo_api.schemas.fields import ImageSensorSchema
from ifdo_api.schemas.image import ImageSchema


class IfdoSchema(BaseModel):
    """Schema for a dataset model, representing a collection of images and their metadata."""

    image_set_header: DatasetSchema = Field(
        default_factory=lambda: (  # noqa: PLC3002
            lambda uid: DatasetSchema(
                uuid=uid,
                name=f"Default Image Set: {uid}",
                handle=f"http://example.com/{uid}",
            )
        )(uuid4())
    )
    image_set_items: dict[str, ImageSchema] = Field(default_factory=dict)


ifdo_addional_fiels_mapping = {
    "image-coordinate-reference-system": "coordinate_reference_system",
    "image-datetime-format": "date_time_format",
}
ifdo_items_mapping = {
    "image-uuid": "uuid",
    "image-handle": "handle",
}

ifdo_header_mapping = {
    "image-set-name": "name",
    "image-set-uuid": "uuid",
    "image-set-handle": "handle",
    "image-set-local-path": "local_path",
    "image-set-min-latitude-degrees": "min_latitude_degrees",
    "image-set-max-latitude-degrees": "max_latitude_degrees",
    "image-set-min-longitude-degrees": "min_longitude_degrees",
    "image-set-max-longitude-degrees": "max_longitude_degrees",
}

ifdo_header_relational_mapping = {
    "image-set-related-materials": "related_materials",
}


ifdo_provenance_mapping = {
    "provenance-agents": "provenance_agents",
    "provenance-entities": "provenance_entities",
    "provenance-activities": "provenance_activities",
}


ifdo_common_relationship_mapping = {
    "image-context": {
        "field_name": "context_id",
        "schema": ImageContextSchema,
        "crud": image_context_crud,
    },
    "image-project": {
        "field_name": "project_id",
        "schema": ImageProjectSchema,
        "crud": image_project_crud,
    },
    "image-event": {"field_name": "event_id", "schema": ImageEventSchema, "crud": image_event_crud},
    "image-platform": {
        "field_name": "platform_id",
        "schema": ImagePlatformSchema,
        "crud": image_platform_crud,
    },
    "image-sensor": {
        "field_name": "sensor_id",
        "schema": ImageSensorSchema,
        "crud": image_sensor_crud,
    },
    "image-pi": {
        "field_name": "pi_id",
        "schema": ImagePISchema,
        "crud": image_pi_crud,
    },
    "image-creators": {
        "field_name": "creators",
        "schema": ImageCreatorSchema,
        "crud": image_creator_crud,
    },
    "image-license": {
        "field_name": "license_id",
        "schema": ImageLicenseSchema,
        "crud": image_license_crud,
    },
    "image-camera-pose": {"field_name": "camera_pose_id", "schema": ImageCameraPoseSchema, "crud": image_camera_pose_crud},
    "image-camera-housing-viewport": {
        "field_name": "camera_housing_viewport_id",
        "schema": ImageCameraHousingViewportSchema,
        "crud": image_camera_housing_viewport_crud,
    },
    "image-flatport-parameters": {
        "field_name": "flatport_parameters_id",
        "schema": ImageFlatportParameterSchema,
        "crud": image_flatport_parameter_crud,
    },
    "image-domeport-parameters": {
        "field_name": "domeport_parameters_id",
        "schema": ImageDomeportParameterSchema,
        "crud": image_domeport_parameter_crud,
    },
    "image-camera-calibration-model": {
        "field_name": "camera_calibration_model_id",
        "schema": ImageCameraCalibrationModelSchema,
        "crud": image_camera_calibration_model_crud,
    },
    "image-photometric-calibration": {
        "field_name": "photometric_calibration_id",
        "schema": ImagePhotometricCalibrationSchema,
        "crud": image_photometric_calibration_crud,
    },
}

ifdo_common_mapping = {
    "image-datetime": "date_time",
    "image-latitude": "latitude",
    "image-longitude": "longitude",
    "image-altitude-meters": "altitude_meters",
    "image-coordinate-uncertainty-meters": "coordinate_uncertainty_meters",
    "image-hash-sha256": "sha256_hash",
    "image-abstract": "abstract",
    "image-entropy": "entropy",
    "image-particle-count": "particle_count",
    "image-average-color": "average_color",
    "image-mpeg7-color-layout": "mpeg7_color_layout",
    "image-mpeg7-color-statistic": "mpeg7_color_statistic",
    "image-mpeg7-color-structure": "mpeg7_color_structure",
    "image-mpeg7-dominant-color": "mpeg7_dominant_color",
    "image-mpeg7-edge-histogram": "mpeg7_edge_histogram",
    "image-mpeg7-homogeneous-texture": "mpeg7_homogeneous_texture",
    "image-mpeg7-scalable-color": "mpeg7_scalable_color",
    "image-acquisition": "acquisition",
    "image-quality": "quality",
    "image-deployment": "deployment",
    "image-navigation": "navigation",
    "image-scale-reference": "scale_reference",
    "image-illumination": "illumination",
    "image-pixel-magnitude": "pixel_magnitude",
    "image-marine-zone": "marine_zone",
    "image-spectral-resolution": "spectral_resolution",
    "image-capture-mode": "capture_mode",
    "image-fauna-attraction": "fauna_attraction",
    "image-area-square-meters": "area_square_meters",
    "image-meters-above-ground": "meters_above_ground",
    "image-acquisition-settings": "acquisition_settings",
    "image-camera-yaw-degrees": "camera_yaw_degrees",
    "image-camera-pitch-degrees": "camera_pitch_degrees",
    "image-camera-roll-degrees": "camera_roll_degrees",
    "image-overlap-fraction": "overlap_fraction",
    "image-objective": "objective",
    "image-target-environment": "target_environment",
    "image-target-timescale": "target_timescale",
    "image-spatial-constraints": "spatial_constraints",
    "image-temporal-constraints": "temporal_constraints",
    "image-time-synchronisation": "time_synchronisation",
    "image-item-identification-scheme": "item_identification_scheme",
    "image-curation-protocol": "curation_protocol",
    "image-visual-constraints": "visual_constraints",
}
