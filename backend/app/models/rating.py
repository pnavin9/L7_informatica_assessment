from sqlalchemy import Column, Float, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

from app.db.database import Base

"""SQLAlchemy model for user ratings on movies."""


class Rating(Base):
    """Rating entity.

    Simple numeric score with optional free‑text review, linked to a Movie.
    """

    __tablename__ = "ratings"

    id = Column(Integer, primary_key=True, index=True)
    movie_id = Column(Integer, ForeignKey("movies.id", ondelete="CASCADE"), nullable=False)
    score = Column(Float, nullable=False)  # e.g., 0.0 to 10.0
    review = Column(Text, nullable=True)

    # Relationship
    movie = relationship("Movie", back_populates="ratings")
