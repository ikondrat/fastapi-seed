"""Module provides functions to initialize and manage database."""

import logging
import os
import threading
from contextlib import contextmanager
from typing import Generator

from sqlalchemy.pool import QueuePool
from sqlmodel import Session, SQLModel, create_engine


class DatabaseManager:
    """Manages database connections."""

    _instance = None
    engine = None
    db_file = None
    _lock = threading.RLock()
    _initialized = False

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

    def __new__(
        cls,
        db_file: str = "purple_test.db",
        cleanup_existing: bool = False,
        pool_size: int = 5,
        max_overflow: int = 10,
        timeout: int = 30,
    ):
        """Create a new instance of the DatabaseManager with thread safety.

        Args:
            db_file: Path to the database file
            cleanup_existing: If True, deletes existing database before creating
            pool_size: The number of connections to keep open
            max_overflow: Max connections to create beyond pool_size
            timeout: Seconds to wait for a connection from the pool

        Returns:
            DatabaseManager instance
        """
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._initialized = False  # noqa: SLF001

            instance = cls._instance

            # Only initialize once
            if not instance._initialized:  # noqa: SLF001
                if cleanup_existing:
                    cls.cleanup_database(db_file)

                # Use connection pooling with reasonable defaults
                connect_args = {
                    # DuckDB needs the parameters in a format it understands
                    "read_only": False
                }

                instance.engine = create_engine(
                    f"duckdb:///{db_file}",
                    poolclass=QueuePool,
                    pool_size=pool_size,
                    max_overflow=max_overflow,
                    pool_timeout=timeout,
                    connect_args=connect_args,
                )

                try:
                    # Initialize tables
                    SQLModel.metadata.create_all(instance.engine)
                    instance._initialized = True  # noqa: SLF001
                    instance.db_file = db_file
                    logging.info(f"Database initialized at {db_file}")
                except Exception as e:
                    logging.error(f"Failed to initialize database: {e}")
                    raise

            return instance

    @contextmanager
    def session(self) -> Generator[Session, None, None]:
        """Create a new database session with automatic commit/rollback.

        Yields:
            Active database session

        Raises:
            Exception: If database operations fail
        """
        if not self._initialized:
            raise RuntimeError("Database not properly initialized")

        session = Session(self.engine)
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def dispose(self):
        """Close all connections and dispose of the engine."""
        if hasattr(self, "engine") and self.engine is not None:
            self.engine.dispose()
            logging.info("Database connections disposed")


def get_session():
    """Yield a new session for database operations.

    For use as a FastAPI dependency.
    """
    with DatabaseManager().session() as session:
        yield session
