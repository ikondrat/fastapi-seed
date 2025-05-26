from __future__ import annotations
from uuid import UUID, uuid4
from sqlmodel import Field, SQLModel
from typing import Optional
from datetime import date


class Movie(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    title: str
    release_date: date
    genre: str
    rating: float = Field(default=0.0, ge=0.0, le=10.0)
    hero_id: Optional[UUID] = Field(default=None, foreign_key="hero.id")
