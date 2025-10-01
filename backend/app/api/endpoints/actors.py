"""Actor API endpoints."""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload

from app.api.deps import get_db
from app.models import Actor, Genre, Movie
from app.schemas import Actor as ActorSchema
from app.schemas import ActorCreate, ActorDetail, ActorUpdate

router = APIRouter()


@router.get("/", response_model=List[ActorSchema])
def get_actors(
    genre: Optional[str] = Query(None, description="Filter actors who acted in this genre"),
    movie: Optional[str] = Query(None, description="Filter actors who acted in this movie"),
    search: Optional[str] = Query(None, description="Search in actor name"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
) -> List[ActorSchema]:
    """Get list of actors with optional filters."""
    query = db.query(Actor)

    # Filter by genre - actors who acted in movies of this genre
    if genre:
        query = query.join(Actor.movies).join(Movie.genres).filter(Genre.name.ilike(f"%{genre}%"))

    # Filter by movie title
    if movie:
        query = query.join(Actor.movies).filter(Movie.title.ilike(f"%{movie}%"))

    # Search in name
    if search:
        query = query.filter(Actor.name.ilike(f"%{search}%"))

    actors = query.distinct().offset(skip).limit(limit).all()
    return [ActorSchema.model_validate(actor) for actor in actors]


@router.get("/{actor_id}", response_model=ActorDetail)
def get_actor(actor_id: int, db: Session = Depends(get_db)) -> ActorDetail:
    """Get detailed actor information with their filmography."""
    actor = db.query(Actor).options(joinedload(Actor.movies)).filter(Actor.id == actor_id).first()

    if not actor:
        raise HTTPException(status_code=404, detail="Actor not found")

    return actor


@router.post("/", response_model=ActorSchema, status_code=201)
def create_actor(actor_data: ActorCreate, db: Session = Depends(get_db)) -> ActorSchema:
    """Create a new actor."""
    actor = Actor(**actor_data.model_dump())
    db.add(actor)
    db.commit()
    db.refresh(actor)
    return actor


@router.put("/{actor_id}", response_model=ActorSchema)
def update_actor(
    actor_id: int, actor_data: ActorUpdate, db: Session = Depends(get_db)
) -> ActorSchema:
    """Update an existing actor."""
    actor = db.query(Actor).filter(Actor.id == actor_id).first()
    if not actor:
        raise HTTPException(status_code=404, detail="Actor not found")

    update_data = actor_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(actor, field, value)

    db.commit()
    db.refresh(actor)
    return actor


@router.delete("/{actor_id}", status_code=204)
def delete_actor(actor_id: int, db: Session = Depends(get_db)) -> None:
    """Delete an actor."""
    actor = db.query(Actor).filter(Actor.id == actor_id).first()
    if not actor:
        raise HTTPException(status_code=404, detail="Actor not found")

    db.delete(actor)
    db.commit()
    return None
