"""Genre API endpoints."""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models import Genre
from app.schemas import Genre as GenreSchema
from app.schemas import GenreCreate, GenreUpdate

router = APIRouter()


@router.get("/", response_model=List[GenreSchema])
def get_genres(
    search: Optional[str] = Query(None, description="Search in genre name"),
    db: Session = Depends(get_db),
) -> List[GenreSchema]:
    """Get list of all genres."""
    query = db.query(Genre)

    if search:
        query = query.filter(Genre.name.ilike(f"%{search}%"))

    genres = query.all()
    return [GenreSchema.model_validate(genre) for genre in genres]


@router.get("/{genre_id}", response_model=GenreSchema)
def get_genre(genre_id: int, db: Session = Depends(get_db)) -> GenreSchema:
    """Get a specific genre by ID."""
    genre = db.query(Genre).filter(Genre.id == genre_id).first()

    if not genre:
        raise HTTPException(status_code=404, detail="Genre not found")

    return genre


@router.post("/", response_model=GenreSchema, status_code=201)
def create_genre(genre_data: GenreCreate, db: Session = Depends(get_db)) -> GenreSchema:
    """Create a new genre."""
    # Check if genre already exists
    existing = db.query(Genre).filter(Genre.name == genre_data.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Genre already exists")

    genre = Genre(**genre_data.model_dump())
    db.add(genre)
    db.commit()
    db.refresh(genre)
    return genre


@router.put("/{genre_id}", response_model=GenreSchema)
def update_genre(
    genre_id: int, genre_data: GenreUpdate, db: Session = Depends(get_db)
) -> GenreSchema:
    """Update an existing genre."""
    genre = db.query(Genre).filter(Genre.id == genre_id).first()
    if not genre:
        raise HTTPException(status_code=404, detail="Genre not found")

    update_data = genre_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(genre, field, value)

    db.commit()
    db.refresh(genre)
    return genre


@router.delete("/{genre_id}", status_code=204)
def delete_genre(genre_id: int, db: Session = Depends(get_db)) -> None:
    """Delete a genre."""
    genre = db.query(Genre).filter(Genre.id == genre_id).first()
    if not genre:
        raise HTTPException(status_code=404, detail="Genre not found")

    db.delete(genre)
    db.commit()
    return None
