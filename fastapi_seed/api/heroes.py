"""Heroes routes module."""

from typing import List

from fastapi import APIRouter, Depends

from fastapi_seed.api.dependencies.services import get_heroes_service
from fastapi_seed.models.hero import Hero, HeroCreate
from fastapi_seed.services.heroes import HeroesService

router = APIRouter(prefix="/heroes", tags=["heroes"])


@router.post("/")
def create_hero(
    hero_create: HeroCreate,
    service: HeroesService = Depends(get_heroes_service),  # noqa: B008
):
    """Create a new hero."""
    return service.create_hero(hero_create)


@router.get("/", response_model=List[Hero])
def read_heroes(
    service: HeroesService = Depends(get_heroes_service),  # noqa: B008
):
    """Read heroes with pagination."""
    return service.get_heroes()
