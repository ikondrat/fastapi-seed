from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from uuid import UUID

from fastapi_seed.repository.db import DatabaseManager
from fastapi_seed.models.movie import Movie, MovieInput, MovieView
from fastapi_seed.models.hero import Hero

router = APIRouter(prefix="/movies", tags=["movies"])


def get_session():
    """Yield a new session for database operations."""
    with DatabaseManager().session() as session:
        yield session


@router.post("/", response_model=MovieView)
def create_movie(movie_input: MovieInput, session: Session = Depends(get_session)):
    movie = Movie.model_validate(movie_input)
    session.add(movie)
    session.commit()
    session.refresh(movie)
    return movie


@router.get("/", response_model=List[Movie])
def read_movies(
    skip: int = 0, limit: int = 100, session: Session = Depends(get_session)
):
    # Use select with join to get movies with their heroes
    statement = select(Movie).offset(skip).limit(limit)
    movies = session.exec(statement).all()
    return movies


@router.put("/{movie_id}/assign-hero/{hero_id}", response_model=Movie)
def assign_hero_to_movie(
    movie_id: UUID, hero_id: UUID, session: Session = Depends(get_session)
):
    movie = session.get(Movie, movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")

    hero.movie_id = movie_id
    session.add(hero)
    session.commit()
    session.refresh(movie)
    return movie
