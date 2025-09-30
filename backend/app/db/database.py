"""
Database configuration and session management.

Schema inspired by IMDb database structure:
https://www.researchgate.net/figure/Complete-schema-of-the-IMDb-database-with-8-main-relations-movie-person-genre_fig1_348079657
"""
import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Use environment variable for database path (Docker-friendly)
# Default to ./movies.db for local development, /code/data/movies.db for Docker
DB_PATH = os.getenv("DATABASE_PATH", "./movies.db")
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def init_db() -> None:
    """Initialize database tables."""
    # Import models to register them with Base.metadata
    # This must be done inside the function to avoid circular imports
    from app.models import Actor, Director, Genre, Movie, Rating  # noqa: F401

    Base.metadata.create_all(bind=engine)
