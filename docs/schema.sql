--
-- PostgreSQL database dump
--

-- Dumped from database version 16.9 (Debian 16.9-1.pgdg110+1)
-- Dumped by pg_dump version 16.9 (Debian 16.9-1.pgdg110+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: tiger; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA tiger;


--
-- Name: tiger_data; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA tiger_data;


--
-- Name: topology; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA topology;


--
-- Name: SCHEMA topology; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON SCHEMA topology IS 'PostGIS Topology schema';


--
-- Name: fuzzystrmatch; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS fuzzystrmatch WITH SCHEMA public;


--
-- Name: EXTENSION fuzzystrmatch; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION fuzzystrmatch IS 'determine similarities and distance between strings';


--
-- Name: postgis; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS postgis WITH SCHEMA public;


--
-- Name: EXTENSION postgis; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION postgis IS 'PostGIS geometry and geography spatial types and functions';


--
-- Name: postgis_tiger_geocoder; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS postgis_tiger_geocoder WITH SCHEMA tiger;


--
-- Name: EXTENSION postgis_tiger_geocoder; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION postgis_tiger_geocoder IS 'PostGIS tiger geocoder and reverse geocoder';


--
-- Name: postgis_topology; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS postgis_topology WITH SCHEMA topology;


--
-- Name: EXTENSION postgis_topology; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION postgis_topology IS 'PostGIS topology spatial types and functions';


--
-- Name: acquisitionenum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.acquisitionenum AS ENUM (
    'photo',
    'video',
    'slide'
);


--
-- Name: capturemodeenum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.capturemodeenum AS ENUM (
    'timer',
    'manual',
    'mixed'
);


--
-- Name: deploymentenum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.deploymentenum AS ENUM (
    'mapping',
    'stationary',
    'survey',
    'exploration',
    'experiment',
    'sampling'
);


--
-- Name: faunaattractionenum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.faunaattractionenum AS ENUM (
    'none',
    'baited',
    'light'
);


--
-- Name: illuminationenum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.illuminationenum AS ENUM (
    'sunlight',
    'artificial_light',
    'mixed_light'
);


--
-- Name: marinezoneenum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.marinezoneenum AS ENUM (
    'seafloor',
    'water_column',
    'sea_surface',
    'atmosphere',
    'laboratory'
);


--
-- Name: navigationenum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.navigationenum AS ENUM (
    'satellite',
    'beacon',
    'transponder',
    'reconstructed'
);


--
-- Name: pixelmagnitudeenum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.pixelmagnitudeenum AS ENUM (
    'km',
    'hm',
    'dam',
    'm',
    'cm',
    'mm',
    'um'
);


--
-- Name: qualityenum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.qualityenum AS ENUM (
    'raw',
    'processed',
    'product'
);


--
-- Name: scalereferenceenum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.scalereferenceenum AS ENUM (
    'camera_3d',
    'camera_calibrated',
    'laser_marker',
    'optical_flow'
);


--
-- Name: shapeenum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.shapeenum AS ENUM (
    'single_pixel',
    'polyline',
    'polygon',
    'circle',
    'rectangle',
    'ellipse',
    'whole_image'
);


--
-- Name: spectralresenum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.spectralresenum AS ENUM (
    'grayscale',
    'rgb',
    'multi_spectral',
    'hyper_spectral'
);


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


--
-- Name: annotation_labels; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.annotation_labels (
    label_id uuid NOT NULL,
    annotation_id uuid NOT NULL,
    annotator_id uuid,
    creation_datetime character varying NOT NULL,
    id uuid NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: annotation_set_creators; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.annotation_set_creators (
    annotation_set_id uuid NOT NULL,
    creator_id uuid NOT NULL
);


--
-- Name: annotation_set_image_sets; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.annotation_set_image_sets (
    annotation_set_id uuid NOT NULL,
    image_set_id uuid NOT NULL
);


--
-- Name: annotation_sets; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.annotation_sets (
    context_id uuid,
    project_id uuid,
    pi_id uuid,
    license_id uuid,
    version character varying(50),
    name character varying(255) NOT NULL,
    handle character varying,
    copyright character varying(500),
    abstract text,
    objective text,
    target_environment text,
    target_timescale text,
    curation_protocol text,
    id uuid NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: annotations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.annotations (
    image_id uuid NOT NULL,
    annotation_platform character varying(255),
    shape public.shapeenum NOT NULL,
    coordinates jsonb NOT NULL,
    annotation_set_id uuid NOT NULL,
    id uuid NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: annotators; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.annotators (
    name character varying(255) NOT NULL,
    id uuid NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: contexts; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.contexts (
    id uuid NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL,
    name character varying(255) NOT NULL,
    uri character varying
);


--
-- Name: creators; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.creators (
    id uuid NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL,
    name character varying(255) NOT NULL,
    uri character varying
);


--
-- Name: events; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.events (
    id uuid NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL,
    name character varying(255) NOT NULL,
    uri character varying
);


--
-- Name: image_camera_calibration_models; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.image_camera_calibration_models (
    calibration_model_type character varying(100),
    focal_length_xy_pixel double precision[],
    principal_point_xy_pixel double precision[],
    distortion_coefficients double precision[],
    approximate_field_of_view_water_xy_degree double precision[],
    extra_description text,
    id uuid NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: image_camera_housing_viewports; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.image_camera_housing_viewports (
    viewport_type character varying(100),
    optical_density double precision,
    thickness_millimeters double precision,
    extra_description text,
    id uuid NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: image_camera_poses; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.image_camera_poses (
    utm_zone character varying(10),
    utm_epsg character varying(10),
    utm_east_north_up_meters double precision[],
    absolute_orientation_utm_matrix double precision[],
    id uuid NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: image_creators; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.image_creators (
    image_id uuid NOT NULL,
    creator_id uuid NOT NULL
);


--
-- Name: image_domeport_parameters; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.image_domeport_parameters (
    outer_radius_millimeters double precision,
    decentering_offset_xyz_millimeters double precision[],
    extra_description text,
    id uuid NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: image_flatport_parameters; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.image_flatport_parameters (
    lens_port_distance_millimeters double precision,
    interface_normal_direction double precision[],
    extra_description text,
    id uuid NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: image_photometric_calibrations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.image_photometric_calibrations (
    sequence_white_balancing text,
    exposure_factor_rgb double precision[],
    sequence_illumination_type character varying(100),
    sequence_illumination_description text,
    illumination_factor_rgb double precision[],
    water_properties_description text,
    id uuid NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: image_set_creators; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.image_set_creators (
    image_set_id uuid NOT NULL,
    creator_id uuid NOT NULL
);


--
-- Name: image_set_related_materials; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.image_set_related_materials (
    image_set_id uuid NOT NULL,
    material_id uuid NOT NULL
);


--
-- Name: image_sets; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.image_sets (
    context_id uuid,
    project_id uuid,
    event_id uuid,
    platform_id uuid,
    sensor_id uuid,
    pi_id uuid,
    license_id uuid,
    camera_pose_id uuid,
    camera_housing_viewport_id uuid,
    flatport_parameter_id uuid,
    domeport_parameter_id uuid,
    photometric_calibration_id uuid,
    camera_calibration_model_id uuid,
    local_path character varying(500),
    min_latitude_degrees double precision,
    max_latitude_degrees double precision,
    min_longitude_degrees double precision,
    max_longitude_degrees double precision,
    limits public.geometry(Polygon,4326),
    name character varying(255) NOT NULL,
    handle character varying,
    copyright character varying(500),
    abstract text,
    objective text,
    target_environment text,
    target_timescale text,
    curation_protocol text,
    sha256_hash character varying(64),
    date_time timestamp without time zone,
    geom public.geometry(Point,4326),
    latitude double precision,
    longitude double precision,
    altitude_meters double precision,
    coordinate_uncertainty_meters double precision,
    entropy double precision,
    particle_count integer,
    average_color double precision[],
    mpeg7_color_layout double precision[],
    mpeg7_color_statistic double precision[],
    mpeg7_color_structure double precision[],
    mpeg7_dominant_color double precision[],
    mpeg7_edge_histogram double precision[],
    mpeg7_homogeneous_texture double precision[],
    mpeg7_scalable_color double precision[],
    acquisition public.acquisitionenum,
    quality public.qualityenum,
    deployment public.deploymentenum,
    navigation public.navigationenum,
    scale_reference public.scalereferenceenum,
    illumination public.illuminationenum,
    pixel_magnitude public.pixelmagnitudeenum,
    marine_zone public.marinezoneenum,
    spectral_resolution public.spectralresenum,
    capture_mode public.capturemodeenum,
    fauna_attraction public.faunaattractionenum,
    area_square_meters double precision,
    meters_above_ground double precision,
    acquisition_settings jsonb,
    camera_yaw_degrees double precision,
    camera_pitch_degrees double precision,
    camera_roll_degrees double precision,
    overlap_fraction double precision,
    spatial_constraints text,
    temporal_constraints text,
    time_synchronisation text,
    item_identification_scheme text,
    visual_constraints text,
    id uuid NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: images; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.images (
    context_id uuid,
    project_id uuid,
    event_id uuid,
    platform_id uuid,
    sensor_id uuid,
    pi_id uuid,
    license_id uuid,
    camera_pose_id uuid,
    camera_housing_viewport_id uuid,
    flatport_parameter_id uuid,
    domeport_parameter_id uuid,
    photometric_calibration_id uuid,
    camera_calibration_model_id uuid,
    image_set_id uuid NOT NULL,
    id uuid NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL,
    name character varying(255) NOT NULL,
    handle character varying,
    copyright character varying(500),
    abstract text,
    objective text,
    target_environment text,
    target_timescale text,
    curation_protocol text,
    sha256_hash character varying(64),
    date_time timestamp without time zone,
    geom public.geometry(Point,4326),
    latitude double precision,
    longitude double precision,
    altitude_meters double precision,
    coordinate_uncertainty_meters double precision,
    entropy double precision,
    particle_count integer,
    average_color double precision[],
    mpeg7_color_layout double precision[],
    mpeg7_color_statistic double precision[],
    mpeg7_color_structure double precision[],
    mpeg7_dominant_color double precision[],
    mpeg7_edge_histogram double precision[],
    mpeg7_homogeneous_texture double precision[],
    mpeg7_scalable_color double precision[],
    acquisition public.acquisitionenum,
    quality public.qualityenum,
    deployment public.deploymentenum,
    navigation public.navigationenum,
    scale_reference public.scalereferenceenum,
    illumination public.illuminationenum,
    pixel_magnitude public.pixelmagnitudeenum,
    marine_zone public.marinezoneenum,
    spectral_resolution public.spectralresenum,
    capture_mode public.capturemodeenum,
    fauna_attraction public.faunaattractionenum,
    area_square_meters double precision,
    meters_above_ground double precision,
    acquisition_settings jsonb,
    camera_yaw_degrees double precision,
    camera_pitch_degrees double precision,
    camera_roll_degrees double precision,
    overlap_fraction double precision,
    spatial_constraints text,
    temporal_constraints text,
    time_synchronisation text,
    item_identification_scheme text,
    visual_constraints text
);


--
-- Name: labels; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.labels (
    name character varying(255) NOT NULL,
    parent_label_name character varying(255) NOT NULL,
    lowest_taxonomic_name character varying(255),
    lowest_aphia_id character varying(50),
    name_is_lowest boolean NOT NULL,
    identification_qualifier character varying(255),
    annotation_set_id uuid NOT NULL,
    id uuid NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: licenses; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.licenses (
    id uuid NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL,
    name character varying(255) NOT NULL,
    uri character varying
);


--
-- Name: pis; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.pis (
    id uuid NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL,
    name character varying(255) NOT NULL,
    uri character varying
);


--
-- Name: platforms; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.platforms (
    id uuid NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL,
    name character varying(255) NOT NULL,
    uri character varying
);


--
-- Name: projects; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.projects (
    id uuid NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL,
    name character varying(255) NOT NULL,
    uri character varying
);


--
-- Name: related_materials; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.related_materials (
    uri character varying,
    title character varying(255),
    relation text,
    id uuid NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: sensors; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.sensors (
    id uuid NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL,
    name character varying(255) NOT NULL,
    uri character varying
);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: annotation_labels annotation_labels_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.annotation_labels
    ADD CONSTRAINT annotation_labels_id_key UNIQUE (id);


--
-- Name: annotation_labels annotation_labels_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.annotation_labels
    ADD CONSTRAINT annotation_labels_pkey PRIMARY KEY (id);


--
-- Name: annotation_set_creators annotation_set_creators_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.annotation_set_creators
    ADD CONSTRAINT annotation_set_creators_pkey PRIMARY KEY (annotation_set_id, creator_id);


--
-- Name: annotation_set_image_sets annotation_set_image_sets_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.annotation_set_image_sets
    ADD CONSTRAINT annotation_set_image_sets_pkey PRIMARY KEY (annotation_set_id, image_set_id);


--
-- Name: annotation_sets annotation_sets_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.annotation_sets
    ADD CONSTRAINT annotation_sets_id_key UNIQUE (id);


--
-- Name: annotation_sets annotation_sets_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.annotation_sets
    ADD CONSTRAINT annotation_sets_name_key UNIQUE (name);


--
-- Name: annotation_sets annotation_sets_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.annotation_sets
    ADD CONSTRAINT annotation_sets_pkey PRIMARY KEY (id);


--
-- Name: annotations annotations_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.annotations
    ADD CONSTRAINT annotations_id_key UNIQUE (id);


--
-- Name: annotations annotations_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.annotations
    ADD CONSTRAINT annotations_pkey PRIMARY KEY (id);


--
-- Name: annotators annotators_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.annotators
    ADD CONSTRAINT annotators_id_key UNIQUE (id);


--
-- Name: annotators annotators_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.annotators
    ADD CONSTRAINT annotators_name_key UNIQUE (name);


--
-- Name: annotators annotators_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.annotators
    ADD CONSTRAINT annotators_pkey PRIMARY KEY (id);


--
-- Name: contexts contexts_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.contexts
    ADD CONSTRAINT contexts_id_key UNIQUE (id);


--
-- Name: contexts contexts_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.contexts
    ADD CONSTRAINT contexts_name_key UNIQUE (name);


--
-- Name: contexts contexts_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.contexts
    ADD CONSTRAINT contexts_pkey PRIMARY KEY (id);


--
-- Name: creators creators_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.creators
    ADD CONSTRAINT creators_id_key UNIQUE (id);


--
-- Name: creators creators_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.creators
    ADD CONSTRAINT creators_name_key UNIQUE (name);


--
-- Name: creators creators_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.creators
    ADD CONSTRAINT creators_pkey PRIMARY KEY (id);


--
-- Name: events events_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.events
    ADD CONSTRAINT events_id_key UNIQUE (id);


--
-- Name: events events_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.events
    ADD CONSTRAINT events_name_key UNIQUE (name);


--
-- Name: events events_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.events
    ADD CONSTRAINT events_pkey PRIMARY KEY (id);


--
-- Name: image_camera_calibration_models image_camera_calibration_models_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.image_camera_calibration_models
    ADD CONSTRAINT image_camera_calibration_models_id_key UNIQUE (id);


--
-- Name: image_camera_calibration_models image_camera_calibration_models_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.image_camera_calibration_models
    ADD CONSTRAINT image_camera_calibration_models_pkey PRIMARY KEY (id);


--
-- Name: image_camera_housing_viewports image_camera_housing_viewports_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.image_camera_housing_viewports
    ADD CONSTRAINT image_camera_housing_viewports_id_key UNIQUE (id);


--
-- Name: image_camera_housing_viewports image_camera_housing_viewports_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.image_camera_housing_viewports
    ADD CONSTRAINT image_camera_housing_viewports_pkey PRIMARY KEY (id);


--
-- Name: image_camera_poses image_camera_poses_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.image_camera_poses
    ADD CONSTRAINT image_camera_poses_id_key UNIQUE (id);


--
-- Name: image_camera_poses image_camera_poses_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.image_camera_poses
    ADD CONSTRAINT image_camera_poses_pkey PRIMARY KEY (id);


--
-- Name: image_creators image_creators_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.image_creators
    ADD CONSTRAINT image_creators_pkey PRIMARY KEY (image_id, creator_id);


--
-- Name: image_domeport_parameters image_domeport_parameters_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.image_domeport_parameters
    ADD CONSTRAINT image_domeport_parameters_id_key UNIQUE (id);


--
-- Name: image_domeport_parameters image_domeport_parameters_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.image_domeport_parameters
    ADD CONSTRAINT image_domeport_parameters_pkey PRIMARY KEY (id);


--
-- Name: image_flatport_parameters image_flatport_parameters_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.image_flatport_parameters
    ADD CONSTRAINT image_flatport_parameters_id_key UNIQUE (id);


--
-- Name: image_flatport_parameters image_flatport_parameters_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.image_flatport_parameters
    ADD CONSTRAINT image_flatport_parameters_pkey PRIMARY KEY (id);


--
-- Name: image_photometric_calibrations image_photometric_calibrations_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.image_photometric_calibrations
    ADD CONSTRAINT image_photometric_calibrations_id_key UNIQUE (id);


--
-- Name: image_photometric_calibrations image_photometric_calibrations_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.image_photometric_calibrations
    ADD CONSTRAINT image_photometric_calibrations_pkey PRIMARY KEY (id);


--
-- Name: image_set_creators image_set_creators_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.image_set_creators
    ADD CONSTRAINT image_set_creators_pkey PRIMARY KEY (image_set_id, creator_id);


--
-- Name: image_set_related_materials image_set_related_materials_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.image_set_related_materials
    ADD CONSTRAINT image_set_related_materials_pkey PRIMARY KEY (image_set_id, material_id);


--
-- Name: image_sets image_sets_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.image_sets
    ADD CONSTRAINT image_sets_id_key UNIQUE (id);


--
-- Name: image_sets image_sets_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.image_sets
    ADD CONSTRAINT image_sets_name_key UNIQUE (name);


--
-- Name: image_sets image_sets_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.image_sets
    ADD CONSTRAINT image_sets_pkey PRIMARY KEY (id);


--
-- Name: image_sets image_sets_sha256_hash_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.image_sets
    ADD CONSTRAINT image_sets_sha256_hash_key UNIQUE (sha256_hash);


--
-- Name: images images_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.images
    ADD CONSTRAINT images_id_key UNIQUE (id);


--
-- Name: images images_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.images
    ADD CONSTRAINT images_name_key UNIQUE (name);


--
-- Name: images images_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.images
    ADD CONSTRAINT images_pkey PRIMARY KEY (id);


--
-- Name: images images_sha256_hash_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.images
    ADD CONSTRAINT images_sha256_hash_key UNIQUE (sha256_hash);


--
-- Name: labels labels_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.labels
    ADD CONSTRAINT labels_id_key UNIQUE (id);


--
-- Name: labels labels_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.labels
    ADD CONSTRAINT labels_name_key UNIQUE (name);


--
-- Name: labels labels_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.labels
    ADD CONSTRAINT labels_pkey PRIMARY KEY (id);


--
-- Name: licenses licenses_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.licenses
    ADD CONSTRAINT licenses_id_key UNIQUE (id);


--
-- Name: licenses licenses_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.licenses
    ADD CONSTRAINT licenses_name_key UNIQUE (name);


--
-- Name: licenses licenses_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.licenses
    ADD CONSTRAINT licenses_pkey PRIMARY KEY (id);


--
-- Name: pis pis_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pis
    ADD CONSTRAINT pis_id_key UNIQUE (id);


--
-- Name: pis pis_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pis
    ADD CONSTRAINT pis_name_key UNIQUE (name);


--
-- Name: pis pis_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pis
    ADD CONSTRAINT pis_pkey PRIMARY KEY (id);


--
-- Name: platforms platforms_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.platforms
    ADD CONSTRAINT platforms_id_key UNIQUE (id);


--
-- Name: platforms platforms_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.platforms
    ADD CONSTRAINT platforms_name_key UNIQUE (name);


--
-- Name: platforms platforms_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.platforms
    ADD CONSTRAINT platforms_pkey PRIMARY KEY (id);


--
-- Name: projects projects_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.projects
    ADD CONSTRAINT projects_id_key UNIQUE (id);


--
-- Name: projects projects_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.projects
    ADD CONSTRAINT projects_name_key UNIQUE (name);


--
-- Name: projects projects_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.projects
    ADD CONSTRAINT projects_pkey PRIMARY KEY (id);


--
-- Name: related_materials related_materials_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.related_materials
    ADD CONSTRAINT related_materials_id_key UNIQUE (id);


--
-- Name: related_materials related_materials_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.related_materials
    ADD CONSTRAINT related_materials_pkey PRIMARY KEY (id);


--
-- Name: sensors sensors_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sensors
    ADD CONSTRAINT sensors_id_key UNIQUE (id);


--
-- Name: sensors sensors_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sensors
    ADD CONSTRAINT sensors_name_key UNIQUE (name);


--
-- Name: sensors sensors_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sensors
    ADD CONSTRAINT sensors_pkey PRIMARY KEY (id);


--
-- Name: idx_image_sets_geom; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_image_sets_geom ON public.image_sets USING gist (geom);


--
-- Name: idx_image_sets_limits; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_image_sets_limits ON public.image_sets USING gist (limits);


--
-- Name: idx_images_geom; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_images_geom ON public.images USING gist (geom);


--
-- Name: annotation_labels annotation_labels_annotation_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.annotation_labels
    ADD CONSTRAINT annotation_labels_annotation_id_fkey FOREIGN KEY (annotation_id) REFERENCES public.annotations(id) ON DELETE CASCADE;


--
-- Name: annotation_labels annotation_labels_annotator_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.annotation_labels
    ADD CONSTRAINT annotation_labels_annotator_id_fkey FOREIGN KEY (annotator_id) REFERENCES public.annotators(id) ON DELETE SET NULL;


--
-- Name: annotation_labels annotation_labels_label_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.annotation_labels
    ADD CONSTRAINT annotation_labels_label_id_fkey FOREIGN KEY (label_id) REFERENCES public.labels(id) ON DELETE CASCADE;


--
-- Name: annotation_set_creators annotation_set_creators_annotation_set_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.annotation_set_creators
    ADD CONSTRAINT annotation_set_creators_annotation_set_id_fkey FOREIGN KEY (annotation_set_id) REFERENCES public.annotation_sets(id) ON DELETE CASCADE;


--
-- Name: annotation_set_creators annotation_set_creators_creator_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.annotation_set_creators
    ADD CONSTRAINT annotation_set_creators_creator_id_fkey FOREIGN KEY (creator_id) REFERENCES public.creators(id) ON DELETE CASCADE;


--
-- Name: annotation_set_image_sets annotation_set_image_sets_annotation_set_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.annotation_set_image_sets
    ADD CONSTRAINT annotation_set_image_sets_annotation_set_id_fkey FOREIGN KEY (annotation_set_id) REFERENCES public.annotation_sets(id) ON DELETE CASCADE;


--
-- Name: annotation_set_image_sets annotation_set_image_sets_image_set_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.annotation_set_image_sets
    ADD CONSTRAINT annotation_set_image_sets_image_set_id_fkey FOREIGN KEY (image_set_id) REFERENCES public.image_sets(id) ON DELETE CASCADE;


--
-- Name: annotation_sets annotation_sets_context_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.annotation_sets
    ADD CONSTRAINT annotation_sets_context_id_fkey FOREIGN KEY (context_id) REFERENCES public.contexts(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: annotation_sets annotation_sets_license_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.annotation_sets
    ADD CONSTRAINT annotation_sets_license_id_fkey FOREIGN KEY (license_id) REFERENCES public.licenses(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: annotation_sets annotation_sets_pi_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.annotation_sets
    ADD CONSTRAINT annotation_sets_pi_id_fkey FOREIGN KEY (pi_id) REFERENCES public.pis(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: annotation_sets annotation_sets_project_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.annotation_sets
    ADD CONSTRAINT annotation_sets_project_id_fkey FOREIGN KEY (project_id) REFERENCES public.projects(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: annotations annotations_annotation_set_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.annotations
    ADD CONSTRAINT annotations_annotation_set_id_fkey FOREIGN KEY (annotation_set_id) REFERENCES public.annotation_sets(id) ON DELETE CASCADE;


--
-- Name: annotations annotations_image_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.annotations
    ADD CONSTRAINT annotations_image_id_fkey FOREIGN KEY (image_id) REFERENCES public.images(id) ON DELETE CASCADE;


--
-- Name: image_creators image_creators_creator_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.image_creators
    ADD CONSTRAINT image_creators_creator_id_fkey FOREIGN KEY (creator_id) REFERENCES public.creators(id) ON DELETE CASCADE;


--
-- Name: image_creators image_creators_image_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.image_creators
    ADD CONSTRAINT image_creators_image_id_fkey FOREIGN KEY (image_id) REFERENCES public.images(id) ON DELETE CASCADE;


--
-- Name: image_set_creators image_set_creators_creator_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.image_set_creators
    ADD CONSTRAINT image_set_creators_creator_id_fkey FOREIGN KEY (creator_id) REFERENCES public.creators(id) ON DELETE CASCADE;


--
-- Name: image_set_creators image_set_creators_image_set_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.image_set_creators
    ADD CONSTRAINT image_set_creators_image_set_id_fkey FOREIGN KEY (image_set_id) REFERENCES public.image_sets(id) ON DELETE CASCADE;


--
-- Name: image_set_related_materials image_set_related_materials_image_set_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.image_set_related_materials
    ADD CONSTRAINT image_set_related_materials_image_set_id_fkey FOREIGN KEY (image_set_id) REFERENCES public.image_sets(id) ON DELETE CASCADE;


--
-- Name: image_set_related_materials image_set_related_materials_material_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.image_set_related_materials
    ADD CONSTRAINT image_set_related_materials_material_id_fkey FOREIGN KEY (material_id) REFERENCES public.related_materials(id) ON DELETE CASCADE;


--
-- Name: image_sets image_sets_camera_calibration_model_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.image_sets
    ADD CONSTRAINT image_sets_camera_calibration_model_id_fkey FOREIGN KEY (camera_calibration_model_id) REFERENCES public.image_camera_calibration_models(id);


--
-- Name: image_sets image_sets_camera_housing_viewport_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.image_sets
    ADD CONSTRAINT image_sets_camera_housing_viewport_id_fkey FOREIGN KEY (camera_housing_viewport_id) REFERENCES public.image_camera_housing_viewports(id);


--
-- Name: image_sets image_sets_camera_pose_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.image_sets
    ADD CONSTRAINT image_sets_camera_pose_id_fkey FOREIGN KEY (camera_pose_id) REFERENCES public.image_camera_poses(id);


--
-- Name: image_sets image_sets_context_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.image_sets
    ADD CONSTRAINT image_sets_context_id_fkey FOREIGN KEY (context_id) REFERENCES public.contexts(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: image_sets image_sets_domeport_parameter_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.image_sets
    ADD CONSTRAINT image_sets_domeport_parameter_id_fkey FOREIGN KEY (domeport_parameter_id) REFERENCES public.image_domeport_parameters(id);


--
-- Name: image_sets image_sets_event_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.image_sets
    ADD CONSTRAINT image_sets_event_id_fkey FOREIGN KEY (event_id) REFERENCES public.events(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: image_sets image_sets_flatport_parameter_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.image_sets
    ADD CONSTRAINT image_sets_flatport_parameter_id_fkey FOREIGN KEY (flatport_parameter_id) REFERENCES public.image_flatport_parameters(id);


--
-- Name: image_sets image_sets_license_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.image_sets
    ADD CONSTRAINT image_sets_license_id_fkey FOREIGN KEY (license_id) REFERENCES public.licenses(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: image_sets image_sets_photometric_calibration_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.image_sets
    ADD CONSTRAINT image_sets_photometric_calibration_id_fkey FOREIGN KEY (photometric_calibration_id) REFERENCES public.image_photometric_calibrations(id);


--
-- Name: image_sets image_sets_pi_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.image_sets
    ADD CONSTRAINT image_sets_pi_id_fkey FOREIGN KEY (pi_id) REFERENCES public.pis(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: image_sets image_sets_platform_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.image_sets
    ADD CONSTRAINT image_sets_platform_id_fkey FOREIGN KEY (platform_id) REFERENCES public.platforms(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: image_sets image_sets_project_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.image_sets
    ADD CONSTRAINT image_sets_project_id_fkey FOREIGN KEY (project_id) REFERENCES public.projects(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: image_sets image_sets_sensor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.image_sets
    ADD CONSTRAINT image_sets_sensor_id_fkey FOREIGN KEY (sensor_id) REFERENCES public.sensors(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: images images_camera_calibration_model_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.images
    ADD CONSTRAINT images_camera_calibration_model_id_fkey FOREIGN KEY (camera_calibration_model_id) REFERENCES public.image_camera_calibration_models(id);


--
-- Name: images images_camera_housing_viewport_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.images
    ADD CONSTRAINT images_camera_housing_viewport_id_fkey FOREIGN KEY (camera_housing_viewport_id) REFERENCES public.image_camera_housing_viewports(id);


--
-- Name: images images_camera_pose_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.images
    ADD CONSTRAINT images_camera_pose_id_fkey FOREIGN KEY (camera_pose_id) REFERENCES public.image_camera_poses(id);


--
-- Name: images images_context_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.images
    ADD CONSTRAINT images_context_id_fkey FOREIGN KEY (context_id) REFERENCES public.contexts(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: images images_domeport_parameter_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.images
    ADD CONSTRAINT images_domeport_parameter_id_fkey FOREIGN KEY (domeport_parameter_id) REFERENCES public.image_domeport_parameters(id);


--
-- Name: images images_event_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.images
    ADD CONSTRAINT images_event_id_fkey FOREIGN KEY (event_id) REFERENCES public.events(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: images images_flatport_parameter_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.images
    ADD CONSTRAINT images_flatport_parameter_id_fkey FOREIGN KEY (flatport_parameter_id) REFERENCES public.image_flatport_parameters(id);


--
-- Name: images images_image_set_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.images
    ADD CONSTRAINT images_image_set_id_fkey FOREIGN KEY (image_set_id) REFERENCES public.image_sets(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: images images_license_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.images
    ADD CONSTRAINT images_license_id_fkey FOREIGN KEY (license_id) REFERENCES public.licenses(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: images images_photometric_calibration_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.images
    ADD CONSTRAINT images_photometric_calibration_id_fkey FOREIGN KEY (photometric_calibration_id) REFERENCES public.image_photometric_calibrations(id);


--
-- Name: images images_pi_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.images
    ADD CONSTRAINT images_pi_id_fkey FOREIGN KEY (pi_id) REFERENCES public.pis(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: images images_platform_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.images
    ADD CONSTRAINT images_platform_id_fkey FOREIGN KEY (platform_id) REFERENCES public.platforms(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: images images_project_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.images
    ADD CONSTRAINT images_project_id_fkey FOREIGN KEY (project_id) REFERENCES public.projects(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: images images_sensor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.images
    ADD CONSTRAINT images_sensor_id_fkey FOREIGN KEY (sensor_id) REFERENCES public.sensors(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: labels labels_annotation_set_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.labels
    ADD CONSTRAINT labels_annotation_set_id_fkey FOREIGN KEY (annotation_set_id) REFERENCES public.annotation_sets(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

