from uuid import UUID, uuid4
from sqlmodel import Field, SQLModel


class HeroBase(SQLModel):
    id: UUID
    name: str


class Hero(HeroBase, table=True):
    __tablename__ = "heroes"
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str


class HeroCreate(SQLModel):
    name: str


class HeroRead(HeroBase):
    pass
