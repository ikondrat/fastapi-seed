from typing import TYPE_CHECKING, List, Optional, Dict, Any
from uuid import UUID, uuid4
from sqlmodel import Field, SQLModel, Relationship

# Use TYPE_CHECKING to avoid circular imports at runtime
if TYPE_CHECKING:
    from fastapi_seed.repository.models.hero import Hero
else:
    # Create a placeholder for runtime that will be replaced with the real class
    Hero = object  # type: ignore


class Movie(SQLModel, table=True):
    __tablename__ = "movies"
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    title: str

    # Relationship
    heroes: List[Hero] = Relationship(
        back_populates="movie",
    )


class MovieBase(SQLModel):
    id: UUID
    title: str


class MovieInput(SQLModel):
    title: str


class MovieView(SQLModel):
    id: UUID
    title: str
    # Use Dict[str, Any] instead of "Hero" to avoid forward reference issues
    heroes: Optional[List[Dict[str, Any]]] = Field(default_factory=list)

    model_config = {"arbitrary_types_allowed": True}
