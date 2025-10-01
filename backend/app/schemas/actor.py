from typing import TYPE_CHECKING, List, Optional

from pydantic import BaseModel, ConfigDict, Field

if TYPE_CHECKING:
    from .movie import Movie


class ActorBase(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    bio: Optional[str] = None
    photo_url: Optional[str] = Field(None, max_length=500, description="URL to actor photo")


class ActorCreate(ActorBase):
    pass


class ActorUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    bio: Optional[str] = None
    photo_url: Optional[str] = Field(None, max_length=500)


class Actor(ActorBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class ActorDetail(Actor):
    """Actor with their movies."""

    movies: List["Movie"] = []

    model_config = ConfigDict(from_attributes=True)
