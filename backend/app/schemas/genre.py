from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class GenreBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)


class GenreCreate(GenreBase):
    pass


class GenreUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)


class Genre(GenreBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
