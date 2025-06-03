"""FastAPI application for Heroes and Movies API."""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from fastapi_seed.api import heroes
from fastapi_seed.repository.database import DatabaseManager

app = FastAPI(title="Heroes and Movies API")


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Lifespan context manager for FastAPI to manage database connections."""
    # Initialize with appropriate pool size based on your workload
    DatabaseManager(pool_size=10, max_overflow=20)
    yield
    # Properly dispose connections when shutting down
    DatabaseManager().dispose()


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title="Lightly Purple API", version="1.0.0", lifespan=lifespan
    )

    app.include_router(heroes.router)

    return app


app = create_app()
