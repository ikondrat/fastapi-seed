"""Heroes service module."""

from sqlmodel import Session

from fastapi_seed.models.hero import Hero, HeroCreate, HeroRead
from fastapi_seed.repository.heroes import create_hero, get_heroes


class HeroesService:
    """Service for managing heroes."""

    def __init__(self, session: Session) -> None:
        """Initialize the HeroesService with a database session."""
        self.session = session

    def create_hero(self, sample_create: HeroCreate) -> Hero:
        """Create a new hero."""
        return create_hero(self.session, sample_create)

    def get_heroes(self) -> list[HeroRead]:
        """Retrieve all heroes."""
        return get_heroes(self.session)
