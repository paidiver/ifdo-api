import os
import sqlalchemy
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()


def get_db_url(alembic: bool = False, psycopg: bool = True) -> str:
    """Get the database URL from environment variables.

    Args:
        alembic (bool, optional): If True, the URL is created for Alembic migrations. Defaults to False.
        psycopg (bool, optional): If True, uses psycopg2 for PostgreSQL. Defaults to True.

    Returns:
        str: Database URL
    """
    username = os.environ.get("POSTGRES_USER", "myuser")
    password = os.environ.get("POSTGRES_PASSWORD", "mypassword")
    database = os.environ.get("POSTGRES_DB", "paidiver_st3")
    hostname = os.environ.get("POSTGRES_HOST", "localhost")
    port = os.environ.get("POSTGRES_PORT", "5432")
    if alembic:
        hostname = os.environ.get("POSTGRES_HOST_ALEMBIC", "localhost")
        port = os.environ.get("POSTGRES_PORT_ALEMBIC", "5432")

    # Construct the database URL
    if psycopg:
        return f"postgresql+psycopg2://{username}:{password}@{hostname}:{port}/{database}"
    return f"postgres://{username}:{password}@{hostname}:{port}/{database}"


def engine_create(alembic: bool = False) -> sqlalchemy.engine.Engine:
    """Create the engine to connect to the database.

    Args:
        alembic (bool, optional): If True, the engine is created for Alembic migrations. Defaults to False.

    Returns:
        sqlalchemy.engine.Engine: engine
    """
    db_url = get_db_url(alembic)
    return create_engine(db_url)


engine = engine_create()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()
metadata = sqlalchemy.MetaData()
