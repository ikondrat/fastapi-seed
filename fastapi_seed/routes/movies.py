from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from fastapi_seed.datalayer.db import DatabaseManager
from fastapi_seed.datalayer.models.movie import Movie
from fastapi_seed.datalayer.models.hero import Hero

router = APIRouter(prefix="/movies", tags=["movies"])


def get_session():
    """Yield a new session for database operations."""
    with DatabaseManager().session() as session:
        yield session


@router.post("/", response_model=Movie)
def create_movie(movie: Movie, session: Session = Depends(get_session)):
    if movie.hero_id:
        hero = session.get(Hero, movie.hero_id)
        if not hero:
            raise HTTPException(status_code=404, detail="Hero not found")

    session.add(movie)
    session.commit()
    session.refresh(movie)
    return movie


@router.get("/", response_model=List[Movie])
def read_movies(
    skip: int = 0, limit: int = 100, session: Session = Depends(get_session)
):
    movies = session.exec(select(Movie).offset(skip).limit(limit)).all()
    return movies


@router.get("/{movie_id}", response_model=Movie)
def read_movie(movie_id: int, session: Session = Depends(get_session)):
    movie = session.get(Movie, movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie


@router.put("/{movie_id}", response_model=Movie)
def update_movie(
    movie_id: int, movie_update: Movie, session: Session = Depends(get_session)
):
    movie = session.get(Movie, movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    if movie_update.hero_id:
        hero = session.get(Hero, movie_update.hero_id)
        if not hero:
            raise HTTPException(status_code=404, detail="Hero not found")

    movie_data = movie_update.dict(exclude_unset=True)
    for key, value in movie_data.items():
        setattr(movie, key, value)

    session.add(movie)
    session.commit()
    session.refresh(movie)
    return movie


@router.delete("/{movie_id}")
def delete_movie(movie_id: int, session: Session = Depends(get_session)):
    movie = session.get(Movie, movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    session.delete(movie)
    session.commit()
    return {"message": "Movie deleted successfully"}
