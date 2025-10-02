from sqlalchemy import Column, ForeignKey, Integer, String, Table, Text
from sqlalchemy.orm import relationship

from app.db.database import Base


"""SQLAlchemy models for movie entities and association tables.

Defines:
- movie_genres: association for many-to-many Movie↔Genre
- movie_actors: association for many-to-many Movie↔Actor
- Movie: core movie entity with relationships and basic attributes
"""

# Association table for many-to-many relationship between movies and genres
movie_genres = Table(
    "movie_genres",
    Base.metadata,
    Column("movie_id", Integer, ForeignKey("movies.id", ondelete="CASCADE"), primary_key=True),
    Column("genre_id", Integer, ForeignKey("genres.id", ondelete="CASCADE"), primary_key=True),
)

# Association table for many-to-many relationship between movies and actors
movie_actors = Table(
    "movie_actors",
    Base.metadata,
    Column("movie_id", Integer, ForeignKey("movies.id", ondelete="CASCADE"), primary_key=True),
    Column("actor_id", Integer, ForeignKey("actors.id", ondelete="CASCADE"), primary_key=True),
)


class Movie(Base):
    """Movie entity.

    Represents a film with basic metadata and relationships to a single
    director, many actors, many genres, and user ratings.
    """

    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    release_year = Column(Integer, nullable=False, index=True)
    synopsis = Column(Text, nullable=True)
    poster_url = Column(String(500), nullable=True)  # URL to movie poster image
    duration_minutes = Column(Integer, nullable=True)  # Movie duration in minutes
    status = Column(String(50), default="Released")  # Released, Coming Soon, etc.
    director_id = Column(Integer, ForeignKey("directors.id"), nullable=False)

    # Relationships
    director = relationship("Director", back_populates="movies")
    actors = relationship("Actor", secondary=movie_actors, back_populates="movies")
    genres = relationship("Genre", secondary=movie_genres, back_populates="movies")
    ratings = relationship("Rating", back_populates="movie", cascade="all, delete-orphan")
