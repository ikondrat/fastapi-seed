from sqlmodel import Session, select

from fastapi_seed.models.hero import Hero, HeroCreate


def create_hero(session: Session, hero_create: HeroCreate):
    # Create a Hero instance from the HeroInput data
    hero = Hero.model_validate(hero_create)

    # Now add the Hero instance to the session
    session.add(hero)
    session.commit()
    session.refresh(hero)

    return hero


def get_heroes(
    session: Session,
    skip: int = 0,
    limit: int = 100,
):
    # Use select with join to get heroes with their movies
    statement = select(Hero).offset(skip).limit(limit)

    heroes = session.exec(statement).all()
    return heroes
