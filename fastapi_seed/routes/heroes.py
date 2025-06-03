from typing import List
from fastapi import APIRouter, Depends

from fastapi_seed.models.hero import Hero, HeroCreate
from fastapi_seed.routes.dependencies.services import get_heroes_service
from fastapi_seed.services.heroes import HeroesService

router = APIRouter(prefix="/heroes", tags=["heroes"])


@router.post("/")
def create_hero(
    hero_create: HeroCreate, service: HeroesService = Depends(get_heroes_service)
):
    return service.create_hero(hero_create)


@router.get("/", response_model=List[Hero])
def read_heroes(
    skip: int = 0,
    limit: int = 100,
    service: HeroesService = Depends(get_heroes_service),
):
    return service.read_heroes(skip=skip, limit=limit)
