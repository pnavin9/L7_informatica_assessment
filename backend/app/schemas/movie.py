from pydantic import BaseModel, Field, ConfigDict, field_validator, computed_field
from typing import Optional, List
from .genre import Genre
from .actor import Actor
from .director import Director
from .rating import Rating


class MovieBase(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    release_year: int = Field(ge=1888, le=2100, description="Year movie was released")
    synopsis: Optional[str] = None
    poster_url: Optional[str] = Field(None, max_length=500, description="URL to movie poster image")
    duration_minutes: Optional[int] = Field(
        None, ge=1, le=600, description="Movie duration in minutes"
    )
    status: Optional[str] = Field(
        "Released", max_length=50, description="Movie status (Released, Coming Soon, etc.)"
    )
    director_id: int = Field(gt=0)

    @field_validator("release_year")
    @classmethod
    def validate_year(cls, v):
        if v < 1888:  # First motion picture
            raise ValueError("Release year cannot be before 1888")
        if v > 2100:
            raise ValueError("Release year cannot be after 2100")
        return v


class MovieCreate(MovieBase):
    genre_ids: List[int] = Field(default_factory=list, description="List of genre IDs")
    actor_ids: List[int] = Field(default_factory=list, description="List of actor IDs")


class MovieUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    release_year: Optional[int] = Field(None, ge=1888, le=2100)
    synopsis: Optional[str] = None
    poster_url: Optional[str] = Field(None, max_length=500)
    duration_minutes: Optional[int] = Field(None, ge=1, le=600)
    status: Optional[str] = Field(None, max_length=50)
    director_id: Optional[int] = Field(None, gt=0)
    genre_ids: Optional[List[int]] = None
    actor_ids: Optional[List[int]] = None


class Movie(MovieBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class MovieDetail(Movie):
    """Movie with all relationships and computed fields."""

    director: Director
    genres: List[Genre] = []
    actors: List[Actor] = []
    ratings: List[Rating] = []

    model_config = ConfigDict(from_attributes=True)

    @computed_field
    def average_rating(self) -> Optional[float]:
        """Calculate average rating from all ratings."""
        if not self.ratings:
            return None
        avg = sum(r.score for r in self.ratings) / len(self.ratings)
        return round(avg, 1)

    @computed_field
    def rating_count(self) -> int:
        """Get total number of ratings."""
        return len(self.ratings)
