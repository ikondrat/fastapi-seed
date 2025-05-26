from typing import Optional
from uuid import UUID, uuid4
from sqlmodel import Field, Relationship, SQLModel


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
        back_populates="heroes"
    )


class HeroInput(SQLModel):
    name: str


class HeroView(HeroBase):
    pass
