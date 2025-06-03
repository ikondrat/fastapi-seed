from sqlmodel import Session

from fastapi_seed.models.hero import Hero, HeroCreate, HeroRead
from fastapi_seed.repository.heroes import create_hero, get_heroes


class HeroesService:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create_hero(self, sample_create: HeroCreate) -> Hero:
        return create_hero(self.session, sample_create)

    def get_heroes(self) -> list[HeroRead]:
        return get_heroes(self.session)
