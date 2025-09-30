"""Director API endpoints."""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from app.api.deps import get_db
from app.models import Director, Movie, Genre
from app.schemas import Director as DirectorSchema, DirectorDetail, DirectorCreate, DirectorUpdate

router = APIRouter()


@router.get("/", response_model=List[DirectorSchema])
def get_directors(
    genre: Optional[str] = Query(None, description="Filter directors who directed this genre"),
    search: Optional[str] = Query(None, description="Search in director name"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
) -> List[DirectorSchema]:
    """Get list of directors with optional filters."""
    query = db.query(Director)

    # Filter by genre - directors who directed movies of this genre
    if genre:
        query = (
            query.join(Director.movies).join(Movie.genres).filter(Genre.name.ilike(f"%{genre}%"))
        )

    # Search in name
    if search:
        query = query.filter(Director.name.ilike(f"%{search}%"))

    directors = query.distinct().offset(skip).limit(limit).all()
    return [DirectorSchema.model_validate(director) for director in directors]


@router.get("/{director_id}", response_model=DirectorDetail)
def get_director(director_id: int, db: Session = Depends(get_db)) -> DirectorDetail:
    """Get detailed director information with their filmography."""
    director = (
        db.query(Director)
        .options(joinedload(Director.movies))
        .filter(Director.id == director_id)
        .first()
    )

    if not director:
        raise HTTPException(status_code=404, detail="Director not found")

    return director


@router.post("/", response_model=DirectorSchema, status_code=201)
def create_director(director_data: DirectorCreate, db: Session = Depends(get_db)) -> DirectorSchema:
    """Create a new director."""
    director = Director(**director_data.model_dump())
    db.add(director)
    db.commit()
    db.refresh(director)
    return director


@router.put("/{director_id}", response_model=DirectorSchema)
def update_director(
    director_id: int, director_data: DirectorUpdate, db: Session = Depends(get_db)
) -> DirectorSchema:
    """Update an existing director."""
    director = db.query(Director).filter(Director.id == director_id).first()
    if not director:
        raise HTTPException(status_code=404, detail="Director not found")

    update_data = director_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(director, field, value)

    db.commit()
    db.refresh(director)
    return director


@router.delete("/{director_id}", status_code=204)
def delete_director(director_id: int, db: Session = Depends(get_db)) -> None:
    """Delete a director."""
    director = db.query(Director).filter(Director.id == director_id).first()
    if not director:
        raise HTTPException(status_code=404, detail="Director not found")

    db.delete(director)
    db.commit()
    return None
