from typing import List
from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from fastapi_seed.datalayer.db import DatabaseManager
from fastapi_seed.datalayer.models.hero import Hero, HeroInput

router = APIRouter(prefix="/heroes", tags=["heroes"])


def get_session():
    """Yield a new session for database operations."""
    with DatabaseManager().session() as session:
        yield session


@router.post("/heroes")
def create_hero(hero_input: HeroInput, session: Session = Depends(get_session)):
    # Create a Hero instance from the HeroInput data
    hero = Hero(name=hero_input.name)

    # Now add the Hero instance to the session
    session.add(hero)
    session.commit()
    session.refresh(hero)

    return hero


@router.get("/", response_model=List[Hero])
def read_heroes(
    skip: int = 0, limit: int = 100, session: Session = Depends(get_session)
):
    # Use select with join to get heroes with their movies
    statement = select(Hero).offset(skip).limit(limit)
    heroes = session.exec(statement).all()
    return heroes
