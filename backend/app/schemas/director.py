from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from .movie import Movie


class DirectorBase(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    bio: Optional[str] = None
    photo_url: Optional[str] = Field(None, max_length=500, description="URL to director photo")


class DirectorCreate(DirectorBase):
    pass


class DirectorUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    bio: Optional[str] = None
    photo_url: Optional[str] = Field(None, max_length=500)


class Director(DirectorBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class DirectorDetail(Director):
    """Director with their movies."""
    movies: List["Movie"] = []

    model_config = ConfigDict(from_attributes=True)
