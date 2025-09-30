"""Movie API endpoints with filtering support."""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_
from app.api.deps import get_db
from app.models import Movie, Genre, Actor, Director
from app.schemas import MovieDetail, Movie as MovieSchema, MovieCreate, MovieUpdate

router = APIRouter()


def apply_movie_filters(query, **filters):
    """Apply filters to movie query in a clean way."""
    # Define filter mappings
    filter_mappings = [
        ('genre', lambda q, v: q.join(Movie.genres).filter(Genre.name.ilike(f"%{v}%"))),
        ('director', lambda q, v: q.join(Movie.director).filter(Director.name.ilike(f"%{v}%"))),
        ('actor', lambda q, v: q.join(Movie.actors).filter(Actor.name.ilike(f"%{v}%"))),
        ('year', lambda q, v: q.filter(Movie.release_year == v)),
        ('min_year', lambda q, v: q.filter(Movie.release_year >= v)),
        ('max_year', lambda q, v: q.filter(Movie.release_year <= v)),
        ('status', lambda q, v: q.filter(Movie.status.ilike(f"%{v}%"))),
        ('search', lambda q, v: q.filter(Movie.title.ilike(f"%{v}%")))
    ]
    
    # Apply filters that have values
    for filter_name, filter_func in filter_mappings:
        if filters.get(filter_name):
            query = filter_func(query, filters[filter_name])
    
    return query


@router.get("/", response_model=List[MovieDetail])
def get_movies(
    genre: Optional[str] = Query(None, description="Filter by genre name"),
    director: Optional[str] = Query(None, description="Filter by director name"),
    actor: Optional[str] = Query(None, description="Filter by actor name"),
    year: Optional[int] = Query(None, description="Filter by release year"),
    min_year: Optional[int] = Query(None, description="Minimum release year"),
    max_year: Optional[int] = Query(None, description="Maximum release year"),
    status: Optional[str] = Query(None, description="Filter by status (Released, Coming Soon, etc.)"),
    search: Optional[str] = Query(None, description="Search in title"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=100, description="Max records to return"),
    db: Session = Depends(get_db)
):
    """
    Get list of movies with optional filters.
    All filtering is performed in the backend using SQLAlchemy queries.
    """
    # Build base query with eager loading
    query = db.query(Movie).options(
        joinedload(Movie.director),
        joinedload(Movie.genres),
        joinedload(Movie.actors),
        joinedload(Movie.ratings)
    )
    
    # Apply filters cleanly
    query = apply_movie_filters(
        query,
        genre=genre,
        director=director,
        actor=actor,
        year=year,
        min_year=min_year,
        max_year=max_year,
        status=status,
        search=search
    )
    
    # Pagination
    movies = query.distinct().offset(skip).limit(limit).all()
    
    # Convert to MovieDetail (computed fields are automatic)
    return [MovieDetail.model_validate(movie) for movie in movies]


@router.get("/{movie_id}", response_model=MovieDetail)
def get_movie(movie_id: int, db: Session = Depends(get_db)):
    """Get detailed movie information by ID."""
    movie = db.query(Movie).options(
        joinedload(Movie.director),
        joinedload(Movie.genres),
        joinedload(Movie.actors),
        joinedload(Movie.ratings)
    ).filter(Movie.id == movie_id).first()
    
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    return MovieDetail.model_validate(movie)


@router.post("/", response_model=MovieSchema, status_code=201)
def create_movie(movie_data: MovieCreate, db: Session = Depends(get_db)):
    """Create a new movie."""
    # Verify director exists
    director = db.query(Director).filter(Director.id == movie_data.director_id).first()
    if not director:
        raise HTTPException(status_code=404, detail="Director not found")
    
    # Create movie
    movie = Movie(
        title=movie_data.title,
        release_year=movie_data.release_year,
        synopsis=movie_data.synopsis,
        poster_url=movie_data.poster_url,
        duration_minutes=movie_data.duration_minutes,
        status=movie_data.status,
        director_id=movie_data.director_id
    )
    
    # Add genres
    if movie_data.genre_ids:
        genres = db.query(Genre).filter(Genre.id.in_(movie_data.genre_ids)).all()
        movie.genres = genres
    
    # Add actors
    if movie_data.actor_ids:
        actors = db.query(Actor).filter(Actor.id.in_(movie_data.actor_ids)).all()
        movie.actors = actors
    
    db.add(movie)
    db.commit()
    db.refresh(movie)
    
    return movie


@router.put("/{movie_id}", response_model=MovieSchema)
def update_movie(movie_id: int, movie_data: MovieUpdate, db: Session = Depends(get_db)):
    """Update an existing movie."""
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    # Update fields
    update_data = movie_data.model_dump(exclude_unset=True)
    
    # Handle genres separately
    if "genre_ids" in update_data:
        genre_ids = update_data.pop("genre_ids")
        if genre_ids is not None:
            genres = db.query(Genre).filter(Genre.id.in_(genre_ids)).all()
            movie.genres = genres
    
    # Handle actors separately
    if "actor_ids" in update_data:
        actor_ids = update_data.pop("actor_ids")
        if actor_ids is not None:
            actors = db.query(Actor).filter(Actor.id.in_(actor_ids)).all()
            movie.actors = actors
    
    # Update remaining fields
    for field, value in update_data.items():
        setattr(movie, field, value)
    
    db.commit()
    db.refresh(movie)
    
    return movie


@router.delete("/{movie_id}", status_code=204)
def delete_movie(movie_id: int, db: Session = Depends(get_db)):
    """Delete a movie."""
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    db.delete(movie)
    db.commit()
    
    return None
