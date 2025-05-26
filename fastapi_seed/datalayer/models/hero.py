from __future__ import annotations
from uuid import UUID, uuid4
from sqlmodel import Field, SQLModel
from typing import Optional


class Hero(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str
    secret_name: str
    age: Optional[int] = None
    power_level: int = Field(default=1, ge=1, le=100)
    is_active: bool = Field(default=True)
