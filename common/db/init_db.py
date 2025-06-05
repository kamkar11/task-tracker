import logging
from typing import Any

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from .database import Base, engine

logger = logging.getLogger(__name__)


def init_db() -> None:
    """Initialize the database, creating all tables."""
    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")

        # Test the connection
        with engine.connect() as connection:
            result: Any = connection.execute(text("SELECT 1"))
            logger.info(f"Database connection test successful: {result.scalar()}")

    except SQLAlchemyError as e:
        logger.error(f"Error initializing database: {e}")
        raise


def drop_db() -> None:
    """Drop all tables. Use with caution!"""
    try:
        Base.metadata.drop_all(bind=engine)
        logger.info("Database tables dropped successfully")
    except SQLAlchemyError as e:
        logger.error(f"Error dropping database tables: {e}")
        raise 