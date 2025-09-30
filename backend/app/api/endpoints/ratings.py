"""Rating API endpoints."""
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.models import Rating, Movie
from app.schemas import Rating as RatingSchema, RatingCreate, RatingUpdate

router = APIRouter()


@router.get("/movies/{movie_id}/ratings", response_model=List[RatingSchema])
def get_movie_ratings(movie_id: int, db: Session = Depends(get_db)):
    """Get all ratings for a specific movie."""
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    ratings = db.query(Rating).filter(Rating.movie_id == movie_id).all()
    return ratings


@router.post("/ratings", response_model=RatingSchema, status_code=201)
def create_rating(rating_data: RatingCreate, db: Session = Depends(get_db)):
    """Create a new rating for a movie."""
    # Verify movie exists
    movie = db.query(Movie).filter(Movie.id == rating_data.movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    rating = Rating(**rating_data.model_dump())
    db.add(rating)
    db.commit()
    db.refresh(rating)
    return rating


@router.put("/ratings/{rating_id}", response_model=RatingSchema)
def update_rating(rating_id: int, rating_data: RatingUpdate, db: Session = Depends(get_db)):
    """Update an existing rating."""
    rating = db.query(Rating).filter(Rating.id == rating_id).first()
    if not rating:
        raise HTTPException(status_code=404, detail="Rating not found")
    
    update_data = rating_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(rating, field, value)
    
    db.commit()
    db.refresh(rating)
    return rating


@router.delete("/ratings/{rating_id}", status_code=204)
def delete_rating(rating_id: int, db: Session = Depends(get_db)):
    """Delete a rating."""
    rating = db.query(Rating).filter(Rating.id == rating_id).first()
    if not rating:
        raise HTTPException(status_code=404, detail="Rating not found")
    
    db.delete(rating)
    db.commit()
    return None
