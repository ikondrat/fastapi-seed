from fastapi import Depends
from sqlmodel import Session

from fastapi_seed.repository.db import get_session
from fastapi_seed.services.heroes import HeroesService


def get_heroes_service(
    session: Session = Depends(get_session),
) -> "HeroesService":
    return HeroesService(session=session)
