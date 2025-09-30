"""Test API endpoints."""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root_endpoint():
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "endpoints" in data


def test_health_check():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_get_movies():
    """Test getting list of movies."""
    response = client.get("/api/movies")
    assert response.status_code == 200
    movies = response.json()
    assert isinstance(movies, list)
    assert len(movies) > 0
    
    # Check movie structure
    movie = movies[0]
    assert "id" in movie
    assert "title" in movie
    assert "release_year" in movie
    assert "director" in movie
    assert "genres" in movie
    assert "actors" in movie
    assert "average_rating" in movie


def test_filter_movies_by_genre():
    """Test filtering movies by genre."""
    response = client.get("/api/movies?genre=Action")
    assert response.status_code == 200
    movies = response.json()
    assert len(movies) > 0
    
    # Verify all movies have Action genre
    for movie in movies:
        genre_names = [g["name"] for g in movie["genres"]]
        assert "Action" in genre_names


def test_filter_movies_by_director():
    """Test filtering movies by director."""
    response = client.get("/api/movies?director=Nolan")
    assert response.status_code == 200
    movies = response.json()
    assert len(movies) > 0
    
    # Verify all movies are by Nolan
    for movie in movies:
        assert "Nolan" in movie["director"]["name"]


def test_filter_movies_by_actor():
    """Test filtering movies by actor."""
    response = client.get("/api/movies?actor=Leonardo")
    assert response.status_code == 200
    movies = response.json()
    assert len(movies) > 0
    
    # Verify all movies have Leonardo DiCaprio
    for movie in movies:
        actor_names = [a["name"] for a in movie["actors"]]
        assert any("Leonardo" in name for name in actor_names)


def test_filter_movies_by_year():
    """Test filtering movies by release year."""
    response = client.get("/api/movies?year=2010")
    assert response.status_code == 200
    movies = response.json()
    
    for movie in movies:
        assert movie["release_year"] == 2010


def test_filter_movies_by_year_range():
    """Test filtering movies by year range."""
    response = client.get("/api/movies?min_year=2015&max_year=2023")
    assert response.status_code == 200
    movies = response.json()
    
    for movie in movies:
        assert 2015 <= movie["release_year"] <= 2023


def test_search_movies():
    """Test searching movies by title."""
    response = client.get("/api/movies?search=Inception")
    assert response.status_code == 200
    movies = response.json()
    assert len(movies) > 0
    assert "Inception" in movies[0]["title"]


def test_get_single_movie():
    """Test getting a single movie by ID."""
    response = client.get("/api/movies/1")
    assert response.status_code == 200
    movie = response.json()
    assert movie["id"] == 1
    assert "title" in movie
    assert "ratings" in movie
    assert isinstance(movie["ratings"], list)


def test_get_nonexistent_movie():
    """Test getting a movie that doesn't exist."""
    response = client.get("/api/movies/9999")
    assert response.status_code == 404


def test_get_actors():
    """Test getting list of actors."""
    response = client.get("/api/actors")
    assert response.status_code == 200
    actors = response.json()
    assert isinstance(actors, list)
    assert len(actors) > 0
    assert "name" in actors[0]


def test_filter_actors_by_genre():
    """Test filtering actors by genre."""
    response = client.get("/api/actors?genre=Action")
    assert response.status_code == 200
    actors = response.json()
    assert len(actors) > 0


def test_get_single_actor():
    """Test getting a single actor with filmography."""
    response = client.get("/api/actors/1")
    assert response.status_code == 200
    actor = response.json()
    assert "name" in actor
    assert "movies" in actor
    assert isinstance(actor["movies"], list)


def test_get_directors():
    """Test getting list of directors."""
    response = client.get("/api/directors")
    assert response.status_code == 200
    directors = response.json()
    assert isinstance(directors, list)
    assert len(directors) > 0


def test_get_single_director():
    """Test getting a single director with filmography."""
    response = client.get("/api/directors/1")
    assert response.status_code == 200
    director = response.json()
    assert "name" in director
    assert "movies" in director
    assert isinstance(director["movies"], list)


def test_get_genres():
    """Test getting list of genres."""
    response = client.get("/api/genres")
    assert response.status_code == 200
    genres = response.json()
    assert isinstance(genres, list)
    assert len(genres) > 0
    assert "name" in genres[0]


def test_get_movie_ratings():
    """Test getting ratings for a specific movie."""
    response = client.get("/api/movies/1/ratings")
    assert response.status_code == 200
    ratings = response.json()
    assert isinstance(ratings, list)
    
    if len(ratings) > 0:
        assert "score" in ratings[0]
        assert "review" in ratings[0]


def test_pagination():
    """Test pagination works correctly."""
    response1 = client.get("/api/movies?limit=5")
    assert response1.status_code == 200
    movies1 = response1.json()
    assert len(movies1) <= 5
    
    response2 = client.get("/api/movies?skip=5&limit=5")
    assert response2.status_code == 200
    movies2 = response2.json()
    
    # Verify different results
    if len(movies2) > 0:
        assert movies1[0]["id"] != movies2[0]["id"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
