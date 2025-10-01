"""Test script to verify database models and relationships."""

from app.db.database import SessionLocal, init_db
from app.db.seed_data import clear_database, seed_database
from app.models import Actor, Director, Genre, Movie


def test_database():
    """Test database models and relationships."""
    # Initialize database and create tables
    init_db()

    # Create a session
    db = SessionLocal()

    try:
        # Clear and seed the database for testing
        clear_database(db)
        seed_database(db)

        # Test 1: Count all movies
        movie_count = db.query(Movie).count()
        assert movie_count > 0, "Should have movies after seeding"

        # Test 2: Get a movie with all relationships
        movie = db.query(Movie).filter(Movie.title == "Inception").first()
        assert movie is not None, "Should find Inception movie"
        assert movie.director is not None, "Movie should have a director"
        assert len(movie.genres) > 0, "Movie should have genres"
        assert len(movie.actors) > 0, "Movie should have actors"
        assert movie.release_year == 2010, "Inception should be from 2010"

        # Test 3: Find movies by director
        nolan = db.query(Director).filter(Director.name == "Christopher Nolan").first()
        assert nolan is not None, "Should find Christopher Nolan"
        assert len(nolan.movies) > 0, "Nolan should have movies"

        # Test 4: Find actors in action movies
        action_genre = db.query(Genre).filter(Genre.name == "Action").first()
        assert action_genre is not None, "Should find Action genre"
        assert len(action_genre.movies) > 0, "Action genre should have movies"

        # Test 5: Actor's filmography
        leo = db.query(Actor).filter(Actor.name == "Leonardo DiCaprio").first()
        assert leo is not None, "Should find Leonardo DiCaprio"
        assert len(leo.movies) > 0, "Leo should have movies"

        # Test 6: Database relationships work correctly
        inception = db.query(Movie).filter(Movie.title == "Inception").first()
        assert inception.director.name == "Christopher Nolan"
        assert "Action" in [g.name for g in inception.genres]
        assert "Leonardo DiCaprio" in [a.name for a in inception.actors]

    finally:
        db.close()


if __name__ == "__main__":
    test_database()
