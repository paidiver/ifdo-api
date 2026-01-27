# iFDO API

<div style="display: flex; align-items: center; gap: 1rem; flex-wrap: wrap;">
  <img src="docs/_static/logo_paidiver.png" alt="iFDO API Logo" style="width: 120px; min-width: 120px;"/>
  <div>
    <strong>iFDO API</strong> is an implementation of the <a href="https://www.ifdo-schema.org/">FAIR Digital Objects for Images (iFDO)</a> specification.
    It provides a standardized way to access, manage, and share image metadata, enabling interoperability between platforms and tools.
    <br><br>
    <strong>Live demo:</strong> <a href="https://api.paidiver.site">https://api.paidiver.site</a>
  </div>
</div>

---

> **Note:** iFDO API is under active development. Features, endpoints, and the API specification may change as improvements are made.

---

## Overview

The iFDO API offers a standardized interface for creating, retrieving, updating, and managing metadata for images.
It uses a **PostGIS** backend for spatial data handling and supports a range of operations that make it easy to integrate image metadata into workflows and applications.

**Version:** 0.1.0 (compatible with all iFDO versions ≥ 2.0.0)

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/paidiver/ifdo-api.git
cd ifdo-api
````

### 2. Configure environment variables

Create a `.env.local` file in the project root:

```bash
POSTGRES_USER=myuser
POSTGRES_PASSWORD=mypassword
POSTGRES_DB=paidiver_st3
POSTGRES_PORT=5432
POSTGRES_HOST=db
REDIS_HOST=redis
REDIS_PORT=6379
```

---

## Running with Docker (recommended)

Running with Docker automatically sets up PostgreSQL, Redis, and other dependencies.

```bash
docker network create shared_network
docker compose -f dockerfiles/docker-compose.yml up -d
```

The API will be available at:
`http://localhost:8081`

**Run database migrations** to create tables and indexes:

```bash
docker compose -f dockerfiles/docker-compose.yml run --rm api poetry run alembic upgrade head
```

**Generate new migration scripts** after modifying models:

```bash
docker compose -f dockerfiles/docker-compose.yml run --rm api poetry run alembic revision --autogenerate -m "Your message here"
```

---

## Running locally (without Docker)

If you prefer to run the API directly:

### 1. Install dependencies

```bash
pip install poetry
poetry install
```

### 2. Start the database

Use PostgreSQL locally or run it via Docker:

```bash
docker compose -f dockerfiles/docker-compose.yml up db
```

### 3. Start Redis

```bash
docker compose -f dockerfiles/docker-compose.yml up redis
```

### 4. Run migrations

```bash
poetry run alembic upgrade head
```

### 5. Start the API server

```bash
poetry run uvicorn ifdo_api.api.app:app --host 0.0.0.0 --port 8081 --reload
```

The API will be available at:
`http://localhost:8081`

> **Note:** When running locally, ensure PostgreSQL and Redis are running, and your `.env.local` matches your setup.

---

## Related Tools

* [iFDO Browser](https://github.com/paidiver/ifdo-browser)
* [STAC API Specification](https://github.com/radiantearth/stac-api-spec)

---

## Acknowledgements

This project was supported by the UK Natural Environment Research Council (NERC) through the
*Tools for automating image analysis for biodiversity monitoring (AIAB)* Funding Opportunity, reference code **UKRI052**.

<!--
## Schemaspy

sudo apt-get update
sudo apt-get install -y graphviz
dot -V

curl -L https://jdbc.postgresql.org/download/postgresql-42.5.4.jar \\n    --output ~/Downloads/jdbc-driver.jar
curl -L https://github.com/schemaspy/schemaspy/releases/download/v7.0.2/schemaspy-app.jar \\n    --output ~/Downloads/schemaspy.jar
java -jar ~/Downloads/schemaspy.jar \
  -t pgsql11 \
  -dp ~/Downloads/jdbc-driver.jar \
  -db paidiver_st3 \
  -host localhost \
  -port 5440 \
  -u myuser \
  -p mypassword \
  -o docs

-->
