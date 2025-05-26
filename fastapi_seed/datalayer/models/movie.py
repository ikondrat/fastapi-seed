from uuid import UUID, uuid4
from sqlmodel import Field, SQLModel, Relationship
from typing import List


class Movie(SQLModel, table=True):
    __tablename__ = "movies"
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    title: str

    # Relationship
    heroes: List["Hero"] = Relationship(  # type: ignore # noqa: F821, E501
        back_populates="movie",
    )


class MovieBase(SQLModel):
    id: UUID
    title: str


class MovieInput(SQLModel):
    title: str


class MovieView(MovieBase):
    pass
