from fastapi import FastAPI
from .datalayer.db import DatabaseManager
from .routes import heroes, movies

app = FastAPI(title="Heroes and Movies API")

# Global instance
db_manager = DatabaseManager(cleanup_existing=True)

# Include routers
app.include_router(heroes.router)
app.include_router(movies.router)
