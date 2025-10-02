from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.database import Base


"""SQLAlchemy model for genres that categorize movies."""


class Genre(Base):
    """Genre entity with unique name.

    Linked to movies via many-to-many association `movie_genres`.
    """

    __tablename__ = "genres"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True, index=True)

    # Many-to-many relationship with movies
    movies = relationship("Movie", secondary="movie_genres", back_populates="genres")
