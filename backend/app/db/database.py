"""
Database configuration and session management.

Schema inspired by IMDb database structure:
https://www.researchgate.net/figure/Complete-schema-of-the-IMDb-database-with-8-main-relations-movie-person-genre_fig1_348079657
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./movies.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def init_db():
    """Initialize database tables."""
    from app.models import Movie, Actor, Director, Genre, Rating
    Base.metadata.create_all(bind=engine)
