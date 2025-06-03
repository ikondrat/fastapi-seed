"""Heroes models."""

from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class HeroBase(SQLModel):
    """Base model for Hero."""

    id: UUID
    name: str


class Hero(HeroBase, table=True):
    """Model for Hero."""

    __tablename__ = "heroes"
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str


class HeroCreate(SQLModel):
    """Model for creating a Hero."""

    name: str


class HeroRead(HeroBase):
    """Model for reading a Hero."""
