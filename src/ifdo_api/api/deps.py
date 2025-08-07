#!/usr/bin/env python3
"""This file contains the dependencies for the FastAPI application."""

from collections.abc import Generator
from ifdo_api.db.db import SessionLocal


def get_db() -> Generator:
    """Get a database session.

    Yields:
        Generator: db session
    """
    db = SessionLocal()
    db.current_user_id = None
    try:
        yield db
    finally:
        db.close()
