from typing import TYPE_CHECKING, Optional
from uuid import UUID, uuid4
from sqlmodel import Field, Relationship, SQLModel

# Use TYPE_CHECKING to avoid circular imports at runtime
if TYPE_CHECKING:
    from fastapi_seed.repository.models.movie import Movie
else:
    # Create a placeholder for runtime that will be replaced with the real class
    Movie = object  # type: ignore


class HeroBase(SQLModel):
    id: UUID
    name: str

    """The dataset ID to which the sample belongs."""
    movie_id: Optional[UUID] = Field(default=None, foreign_key="movies.id")


class Hero(HeroBase, table=True):
    __tablename__ = "heroes"
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str

    movie: Optional["Movie"] = Relationship(  # type: ignore # noqa: F821, E501
        back_populates="heroes",
        sa_relationship_kwargs={"lazy": "select"},
    )


class HeroInput(SQLModel):
    name: str


class HeroView(HeroBase):
    pass
