"""Module provides functions to initialize and manage the DuckDB."""

import logging
import os
from contextlib import contextmanager
from typing import Generator

from sqlmodel import Session, SQLModel, create_engine


class DatabaseManager:
    """Manages database connections and ensures proper resource handling."""

    _instance = None

    @staticmethod
    def database_exists(db_file: str) -> bool:
        """Check if database file exists.

        Args:
            db_file: Path to the database file

        Returns:
            True if database file exists, False otherwise
        """
        return os.path.exists(db_file)

    @staticmethod
    def cleanup_database(db_file: str) -> None:
        """Delete database file if it exists.

        Args:
            db_file: Path to the database file to delete
        """
        if DatabaseManager.database_exists(db_file):
            os.remove(db_file)
            logging.info(f"Deleted existing database: {db_file}")

    def __new__(cls, db_file: str = "purple.db", cleanup_existing: bool = False):
        """Create a new instance of the DatabaseManager.

        Args:
            db_file: Path to the database file
            cleanup_existing: If True, deletes existing database
            before creating a new one

        Returns:
            DatabaseManager instance
        """
        if cleanup_existing:
            cls.cleanup_database(db_file)

        if cls._instance is None:
            cls._instance = super().__new__(cls)
            # File-based DuckDB
            cls._instance.engine = create_engine(f"duckdb:///{db_file}")
            # Initialize tables
            SQLModel.metadata.create_all(cls._instance.engine)
        return cls._instance

    @contextmanager
    def session(self) -> Generator[Session, None, None]:
        """Create a new database session."""
        session = Session(self.engine)
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
