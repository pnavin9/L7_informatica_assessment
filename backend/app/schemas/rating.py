from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class RatingBase(BaseModel):
    score: float = Field(ge=0.0, le=10.0, description="Rating score between 0.0 and 10.0")
    review: Optional[str] = Field(None, max_length=2000)


class RatingCreate(RatingBase):
    movie_id: int = Field(gt=0)


class RatingUpdate(BaseModel):
    score: Optional[float] = Field(None, ge=0.0, le=10.0)
    review: Optional[str] = Field(None, max_length=2000)


class Rating(RatingBase):
    id: int
    movie_id: int

    model_config = ConfigDict(from_attributes=True)
