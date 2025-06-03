"""FastAPI application for Heroes and Movies API."""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from fastapi_seed.api import content_moderation, heroes
from fastapi_seed.repository.database import DatabaseManager
from fastapi_seed.services.content_moderation import ContentModerationService

app = FastAPI(title="Heroes and Movies API")


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Lifespan context manager for FastAPI to manage database connections and services."""
    # Initialize with appropriate pool size based on your workload
    DatabaseManager(pool_size=10, max_overflow=20)

    # Initialize content moderation service and download model
    print("Initializing content moderation service and downloading model...")
    ContentModerationService.initialize()
    print("Content moderation service initialized successfully!")

    yield

    # Properly dispose connections when shutting down
    DatabaseManager().dispose()


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title="Lightly Purple API", version="1.0.0", lifespan=lifespan
    )

    app.include_router(heroes.router)
    app.include_router(content_moderation.router)

    return app


app = create_app()
