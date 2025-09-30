from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from app.db.database import Base


class Actor(Base):
    __tablename__ = "actors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    bio = Column(Text, nullable=True)
    photo_url = Column(String(500), nullable=True)  # URL to actor photo

    # Many-to-many relationship with movies
    movies = relationship("Movie", secondary="movie_actors", back_populates="actors")
