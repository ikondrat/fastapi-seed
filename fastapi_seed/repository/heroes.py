"""Heroes repository module."""

from sqlmodel import Session, select

from fastapi_seed.models.hero import Hero, HeroCreate


def create_hero(session: Session, hero_create: HeroCreate):
    """Create a new hero in the database."""
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
    """Retrieve heroes from the database with pagination."""
    statement = select(Hero).offset(skip).limit(limit)

    return session.exec(statement).all()
