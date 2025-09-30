from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from app.db.database import Base


class Director(Base):
    __tablename__ = "directors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    bio = Column(Text, nullable=True)
    photo_url = Column(String(500), nullable=True)  # URL to director photo

    # Relationship: one director can have many movies
    movies = relationship("Movie", back_populates="director")
