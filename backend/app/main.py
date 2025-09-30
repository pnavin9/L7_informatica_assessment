"""
Main FastAPI application.

Movie Explorer Platform - RESTful API with comprehensive filtering.
"""
from typing import Dict, Any
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.database import init_db
from app.db.seed_data import seed_database
from app.db.database import SessionLocal
from app.api.endpoints import movies, actors, directors, genres, ratings

# Initialize database
init_db()

# Seed database with sample data
db = SessionLocal()
try:
    seed_database(db)
finally:
    db.close()

# Create FastAPI app
app = FastAPI(
    title="Movie Explorer API",
    description="RESTful API for exploring movies, actors, directors, and genres with comprehensive filtering",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(movies.router, prefix="/api/movies", tags=["Movies"])
app.include_router(actors.router, prefix="/api/actors", tags=["Actors"])
app.include_router(directors.router, prefix="/api/directors", tags=["Directors"])
app.include_router(genres.router, prefix="/api/genres", tags=["Genres"])
app.include_router(ratings.router, prefix="/api", tags=["Ratings"])


@app.get("/", tags=["Root"])
def root() -> Dict[str, Any]:
    """Root endpoint with API information."""
    return {
        "message": "Welcome to Movie Explorer API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "movies": "/api/movies",
            "actors": "/api/actors",
            "directors": "/api/directors",
            "genres": "/api/genres",
            "ratings": "/api/ratings"
        }
    }


@app.get("/health", tags=["Health"])
def health_check() -> Dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy"}
