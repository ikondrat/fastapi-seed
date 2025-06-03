"""Routes services module."""

from __future__ import annotations

from fastapi import Depends
from sqlmodel import Session

from fastapi_seed.repository.database import get_session
from fastapi_seed.services.heroes import HeroesService


def get_heroes_service(
    session: Session = Depends(get_session),  # noqa: B008
) -> HeroesService:
    """Get HeroesService instance."""
    return HeroesService(session=session)
