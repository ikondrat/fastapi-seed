from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from fastapi_seed.datalayer.db import DatabaseManager
from fastapi_seed.datalayer.models.hero import Hero

router = APIRouter(prefix="/heroes", tags=["heroes"])


def get_session():
    """Yield a new session for database operations."""
    with DatabaseManager().session() as session:
        yield session


@router.post("/", response_model=Hero)
def create_hero(hero: Hero, session: Session = Depends(get_session)):
    session.add(hero)
    session.commit()
    session.refresh(hero)
    return hero


@router.get("/", response_model=List[Hero])
def read_heroes(
    skip: int = 0, limit: int = 100, session: Session = Depends(get_session)
):
    heroes = session.exec(select(Hero).offset(skip).limit(limit)).all()
    return heroes


@router.get("/{hero_id}", response_model=Hero)
def read_hero(hero_id: int, session: Session = Depends(get_session)):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero


@router.put("/{hero_id}", response_model=Hero)
def update_hero(
    hero_id: int, hero_update: Hero, session: Session = Depends(get_session)
):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")

    hero_data = hero_update.dict(exclude_unset=True)
    for key, value in hero_data.items():
        setattr(hero, key, value)

    session.add(hero)
    session.commit()
    session.refresh(hero)
    return hero


@router.delete("/{hero_id}")
def delete_hero(hero_id: int, session: Session = Depends(get_session)):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")

    session.delete(hero)
    session.commit()
    return {"message": "Hero deleted successfully"}
