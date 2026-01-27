from ifdo_api.crud.fields import context_crud
from ifdo_api.crud.fields import creator_crud
from ifdo_api.crud.fields import event_crud
from ifdo_api.crud.fields import image_camera_calibration_model_crud
from ifdo_api.crud.fields import image_camera_housing_viewport_crud
from ifdo_api.crud.fields import image_camera_pose_crud
from ifdo_api.crud.fields import image_domeport_parameter_crud
from ifdo_api.crud.fields import image_flatport_parameter_crud
from ifdo_api.crud.fields import image_photometric_calibration_crud
from ifdo_api.crud.fields import license_crud
from ifdo_api.crud.fields import pi_crud
from ifdo_api.crud.fields import platform_crud
from ifdo_api.crud.fields import project_crud
from ifdo_api.crud.fields import related_material_crud
from ifdo_api.crud.fields import sensor_crud
from ifdo_api.models.base import AcquisitionEnum
from ifdo_api.models.base import CaptureModeEnum
from ifdo_api.models.base import DeploymentEnum
from ifdo_api.models.base import FaunaAttractionEnum
from ifdo_api.models.base import IlluminationEnum
from ifdo_api.models.base import MarineZoneEnum
from ifdo_api.models.base import NavigationEnum
from ifdo_api.models.base import PixelMagnitudeEnum
from ifdo_api.models.base import QualityEnum
from ifdo_api.models.base import ScaleReferenceEnum
from ifdo_api.models.base import SpectralResEnum
from ifdo_api.schemas.fields import ImageCameraPoseSchema

ifdo_mapping = {
    "image-set-name": {"field_name": "name"},
    "image-set-uuid": {"field_name": "id", "location": "header"},
    "image-set-handle": {"field_name": "handle", "location": "header"},
    "image-set-local-path": {"field_name": "local_path", "location": "header"},
    "image-set-min-latitude-degrees": {"field_name": "min_latitude_degrees", "location": "header"},
    "image-set-max-latitude-degrees": {"field_name": "max_latitude_degrees", "location": "header"},
    "image-set-min-longitude-degrees": {"field_name": "min_longitude_degrees", "location": "header"},
    "image-set-max-longitude-degrees": {"field_name": "max_longitude_degrees", "location": "header"},
    "image-datetime": {"field_name": "date_time", "location": "header"},
    "image-latitude": {
        "field_name": "latitude",
    },
    "image-longitude": {
        "field_name": "longitude",
    },
    "image-altitude-meters": {
        "field_name": "altitude_meters",
    },
    "image-coordinate-uncertainty-meters": {
        "field_name": "coordinate_uncertainty_meters",
    },
    "image-hash-sha256": {"field_name": "sha256_hash"},
    "image-abstract": {"field_name": "abstract"},
    "image-entropy": {"field_name": "entropy"},
    "image-particle-count": {"field_name": "particle_count"},
    "image-average-color": {"field_name": "average_color"},
    "image-mpeg7-color-layout": {"field_name": "mpeg7_color_layout"},
    "image-mpeg7-color-statistic": {"field_name": "mpeg7_color_statistic"},
    "image-mpeg7-color-structure": {"field_name": "mpeg7_color_structure"},
    "image-mpeg7-dominant-color": {"field_name": "mpeg7_dominant_color"},
    "image-mpeg7-edge-histogram": {"field_name": "mpeg7_edge_histogram"},
    "image-mpeg7-homogeneous-texture": {"field_name": "mpeg7_homogeneous_texture"},
    "image-mpeg7-scalable-color": {"field_name": "mpeg7_scalable_color"},
    "image-acquisition": {"field_name": "acquisition", "normalize": AcquisitionEnum},
    "image-quality": {"field_name": "quality", "normalize": QualityEnum},
    "image-deployment": {"field_name": "deployment", "normalize": DeploymentEnum},
    "image-navigation": {"field_name": "navigation", "normalize": NavigationEnum},
    "image-scale-reference": {"field_name": "scale_reference", "normalize": ScaleReferenceEnum},
    "image-illumination": {"field_name": "illumination", "normalize": IlluminationEnum},
    "image-pixel-magnitude": {"field_name": "pixel_magnitude", "normalize": PixelMagnitudeEnum},
    "image-marine-zone": {"field_name": "marine_zone", "normalize": MarineZoneEnum},
    "image-spectral-resolution": {"field_name": "spectral_resolution", "normalize": SpectralResEnum},
    "image-capture-mode": {"field_name": "capture_mode", "normalize": CaptureModeEnum},
    "image-fauna-attraction": {"field_name": "fauna_attraction", "normalize": FaunaAttractionEnum},
    "image-area-square-meters": {"field_name": "area_square_meters"},
    "image-meters-above-ground": {"field_name": "meters_above_ground"},
    "image-acquisition-settings": {"field_name": "acquisition_settings"},
    "image-camera-yaw-degrees": {"field_name": "camera_yaw_degrees"},
    "image-camera-pitch-degrees": {"field_name": "camera_pitch_degrees"},
    "image-camera-roll-degrees": {"field_name": "camera_roll_degrees"},
    "image-overlap-fraction": {"field_name": "overlap_fraction"},
    "image-objective": {"field_name": "objective"},
    "image-target-environment": {"field_name": "target_environment"},
    "image-target-timescale": {"field_name": "target_timescale"},
    "image-spatial-constraints": {"field_name": "spatial_constraints"},
    "image-temporal-constraints": {"field_name": "temporal_constraints"},
    "image-time-synchronisation": {"field_name": "time_synchronisation"},
    "image-item-identification-scheme": {"field_name": "item_identification_scheme"},
    "image-curation-protocol": {"field_name": "curation_protocol"},
    "image-visual-constraints": {"field_name": "visual_constraints"},
    "image-uuid": {"field_name": "id", "location": "items"},
    "image-handle": {"field_name": "handle", "location": "items"},
    "image-context": {
        "field_name": "context",
        "crud": context_crud,
        "unique": "name",
    },
    "image-project": {
        "field_name": "project",
        "crud": project_crud,
        "unique": "name",
    },
    "image-event": {"field_name": "event", "crud": event_crud, "unique": "name"},
    "image-platform": {
        "field_name": "platform",
        "crud": platform_crud,
        "unique": "name",
    },
    "image-sensor": {
        "field_name": "sensor",
        "crud": sensor_crud,
        "unique": "name",
    },
    "image-pi": {
        "field_name": "pi",
        "crud": pi_crud,
        "unique": "name",
    },
    "image-license": {
        "field_name": "license",
        "crud": license_crud,
        "unique": "name",
    },
    "image-camera-pose": {"field_name": "camera_pose", "schema": ImageCameraPoseSchema, "crud": image_camera_pose_crud},
    "image-camera-housing-viewport": {
        "field_name": "camera_housing_viewport",
        "crud": image_camera_housing_viewport_crud,
    },
    "image-flatport-parameters": {
        "field_name": "flatport_parameters",
        "crud": image_flatport_parameter_crud,
    },
    "image-domeport-parameters": {
        "field_name": "domeport_parameters",
        "crud": image_domeport_parameter_crud,
    },
    "image-camera-calibration-model": {
        "field_name": "camera_calibration_model",
        "crud": image_camera_calibration_model_crud,
    },
    "image-photometric-calibration": {
        "field_name": "photometric_calibration",
        "crud": image_photometric_calibration_crud,
    },
    "image-creators": {
        "field_name": "creators",
        "crud": creator_crud,
        "list": True,
        "unique": "name",
    },
    "image-set-related-materials": {
        "field_name": "related_materials",
        "crud": related_material_crud,
        "list": True,
        "location": "header",
    },
}

ifdo_addional_fiels_mapping = {
    "image-coordinate-reference-system": "coordinate_reference_system",
    "image-datetime-format": "date_time_format",
}


# ifdo_provenance_mapping = {
#     "provenance-agents": "provenance_agents",
#     "provenance-entities": "provenance_entities",
#     "provenance-activities": "provenance_activities",
# }
