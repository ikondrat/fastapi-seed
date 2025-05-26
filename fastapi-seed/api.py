from typing import Union

from fastapi import FastAPI
from .datalayer.db import DatabaseManager

app = FastAPI()

# Global instance
db_manager = DatabaseManager(cleanup_existing=True)


# For FastAPI dependency injection
def get_session():
    """Yield a new session for database operations."""
    with db_manager.session() as session:
        yield session


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
