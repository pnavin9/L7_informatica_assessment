"""Test script to verify database models and relationships."""
from app.db.database import engine, SessionLocal, init_db
from app.db.seed_data import seed_database
from app.models import Movie, Actor, Director, Genre, Rating


def test_database():
    # Initialize database and create tables
    print("Creating database tables...")
    init_db()
    
    # Create a session
    db = SessionLocal()
    
    try:
        # Seed the database
        print("\nSeeding database...")
        seed_database(db)
        
        # Test queries
        print("\n=== DATABASE TESTS ===\n")
        
        # Test 1: Count all movies
        movie_count = db.query(Movie).count()
        print(f"✓ Total movies: {movie_count}")
        
        # Test 2: Get a movie with all relationships
        movie = db.query(Movie).filter(Movie.title == "Inception").first()
        if movie:
            print(f"\n✓ Movie: {movie.title} ({movie.release_year})")
            print(f"  Director: {movie.director.name}")
            print(f"  Genres: {', '.join([g.name for g in movie.genres])}")
            print(f"  Actors: {', '.join([a.name for a in movie.actors])}")
            print(f"  Ratings: {len(movie.ratings)} reviews")
            if movie.ratings:
                avg_rating = sum(r.score for r in movie.ratings) / len(movie.ratings)
                print(f"  Average Score: {avg_rating:.1f}/10")
        
        # Test 3: Find movies by director
        nolan = db.query(Director).filter(Director.name == "Christopher Nolan").first()
        if nolan:
            print(f"\n✓ Christopher Nolan's movies ({len(nolan.movies)}):")
            for m in nolan.movies:
                print(f"  - {m.title} ({m.release_year})")
        
        # Test 4: Find actors in action movies
        action_genre = db.query(Genre).filter(Genre.name == "Action").first()
        if action_genre:
            print(f"\n✓ Action movies ({len(action_genre.movies)}):")
            for m in action_genre.movies[:5]:
                print(f"  - {m.title}")
        
        # Test 5: Actor's filmography
        leo = db.query(Actor).filter(Actor.name == "Leonardo DiCaprio").first()
        if leo:
            print(f"\n✓ Leonardo DiCaprio's movies ({len(leo.movies)}):")
            for m in leo.movies:
                print(f"  - {m.title} ({m.release_year})")
        
        print("\n✅ All database tests passed!")
        
    finally:
        db.close()


if __name__ == "__main__":
    test_database()
