"""Test comprehensive filtering logic."""

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


class TestMovieFilters:
    """Test all movie filtering combinations."""

    def test_filter_by_genre_only(self):
        """Test filtering by genre alone."""
        response = client.get("/api/movies?genre=Action")
        assert response.status_code == 200
        movies = response.json()

        for movie in movies:
            genre_names = [g["name"] for g in movie["genres"]]
            assert "Action" in genre_names

    def test_filter_by_director_only(self):
        """Test filtering by director alone."""
        response = client.get("/api/movies?director=Nolan")
        assert response.status_code == 200
        movies = response.json()

        for movie in movies:
            assert "Nolan" in movie["director"]["name"]

    def test_filter_by_actor_only(self):
        """Test filtering by actor alone."""
        response = client.get("/api/movies?actor=DiCaprio")
        assert response.status_code == 200
        movies = response.json()

        for movie in movies:
            actor_names = [a["name"] for a in movie["actors"]]
            assert any("DiCaprio" in name for name in actor_names)

    def test_filter_by_year_only(self):
        """Test filtering by year alone."""
        response = client.get("/api/movies?year=2010")
        assert response.status_code == 200
        movies = response.json()

        for movie in movies:
            assert movie["release_year"] == 2010

    def test_filter_by_min_year_only(self):
        """Test filtering by minimum year."""
        response = client.get("/api/movies?min_year=2015")
        assert response.status_code == 200
        movies = response.json()

        for movie in movies:
            assert movie["release_year"] >= 2015

    def test_filter_by_max_year_only(self):
        """Test filtering by maximum year."""
        response = client.get("/api/movies?max_year=2015")
        assert response.status_code == 200
        movies = response.json()

        for movie in movies:
            assert movie["release_year"] <= 2015

    def test_filter_by_year_range(self):
        """Test filtering by year range."""
        response = client.get("/api/movies?min_year=2010&max_year=2020")
        assert response.status_code == 200
        movies = response.json()

        for movie in movies:
            assert 2010 <= movie["release_year"] <= 2020

    def test_filter_genre_and_year(self):
        """Test combining genre and year filters."""
        response = client.get("/api/movies?genre=Action&year=2010")
        assert response.status_code == 200
        movies = response.json()

        for movie in movies:
            assert movie["release_year"] == 2010
            genre_names = [g["name"] for g in movie["genres"]]
            assert "Action" in genre_names

    def test_filter_director_and_genre(self):
        """Test combining director and genre filters."""
        response = client.get("/api/movies?director=Nolan&genre=Sci-Fi")
        assert response.status_code == 200
        movies = response.json()

        for movie in movies:
            assert "Nolan" in movie["director"]["name"]
            genre_names = [g["name"] for g in movie["genres"]]
            assert "Sci-Fi" in genre_names

    def test_filter_actor_and_year_range(self):
        """Test combining actor and year range filters."""
        response = client.get("/api/movies?actor=DiCaprio&min_year=2010&max_year=2020")
        assert response.status_code == 200
        movies = response.json()

        for movie in movies:
            assert 2010 <= movie["release_year"] <= 2020
            actor_names = [a["name"] for a in movie["actors"]]
            assert any("DiCaprio" in name for name in actor_names)

    def test_filter_all_parameters(self):
        """Test using all filter parameters together."""
        response = client.get(
            "/api/movies?genre=Action&director=Nolan&actor=Bale&min_year=2000&max_year=2020"
        )
        assert response.status_code == 200
        movies = response.json()

        # Verify all filters are applied
        for movie in movies:
            assert 2000 <= movie["release_year"] <= 2020
            assert "Nolan" in movie["director"]["name"]
            genre_names = [g["name"] for g in movie["genres"]]
            assert "Action" in genre_names
            actor_names = [a["name"] for a in movie["actors"]]
            assert any("Bale" in name for name in actor_names)

    def test_search_with_filters(self):
        """Test combining search with filters."""
        response = client.get("/api/movies?search=Knight&genre=Action")
        assert response.status_code == 200
        movies = response.json()

        for movie in movies:
            # Should match search term
            assert "Knight" in movie["title"] or "knight" in movie["title"].lower()
            # Should match filter
            genre_names = [g["name"] for g in movie["genres"]]
            assert "Action" in genre_names

    def test_search_case_insensitive(self):
        """Test search is case-insensitive."""
        response1 = client.get("/api/movies?search=dark")
        response2 = client.get("/api/movies?search=Dark")
        response3 = client.get("/api/movies?search=DARK")

        movies1 = response1.json()
        movies2 = response2.json()
        movies3 = response3.json()

        # All should return the same count
        assert len(movies1) == len(movies2) == len(movies3)

    def test_partial_director_name_match(self):
        """Test partial director name matching."""
        response = client.get("/api/movies?director=Nol")
        assert response.status_code == 200
        movies = response.json()

        for movie in movies:
            assert "Nol" in movie["director"]["name"]

    def test_partial_actor_name_match(self):
        """Test partial actor name matching."""
        response = client.get("/api/movies?actor=Leo")
        assert response.status_code == 200
        movies = response.json()

        for movie in movies:
            actor_names = [a["name"] for a in movie["actors"]]
            assert any("Leo" in name for name in actor_names)

    def test_exact_genre_match(self):
        """Test genre matching is exact (not partial)."""
        response = client.get("/api/movies?genre=Action")
        assert response.status_code == 200
        movies = response.json()

        # Should match "Action" exactly, not "Action-Adventure"
        for movie in movies:
            genre_names = [g["name"] for g in movie["genres"]]
            assert "Action" in genre_names


class TestActorFilters:
    """Test actor filtering."""

    def test_filter_actors_by_genre(self):
        """Test filtering actors by genre they've worked in."""
        response = client.get("/api/actors?genre=Action")
        assert response.status_code == 200
        actors = response.json()

        # Should return actors who have worked in Action movies
        assert isinstance(actors, list)

    def test_actors_with_no_genre_filter(self):
        """Test getting all actors without filter."""
        response = client.get("/api/actors")
        assert response.status_code == 200
        actors = response.json()

        assert len(actors) > 0
        assert "name" in actors[0]


class TestPaginationWithFilters:
    """Test pagination works correctly with filters."""

    def test_pagination_with_genre_filter(self):
        """Test pagination works with genre filter."""
        response1 = client.get("/api/movies?genre=Action&limit=2")
        response2 = client.get("/api/movies?genre=Action&skip=2&limit=2")

        assert response1.status_code == 200
        assert response2.status_code == 200

        movies1 = response1.json()
        movies2 = response2.json()

        # Should get different movies
        if len(movies2) > 0:
            assert movies1[0]["id"] != movies2[0]["id"]

    def test_pagination_with_search(self):
        """Test pagination works with search."""
        response1 = client.get("/api/movies?search=The&limit=3")
        response2 = client.get("/api/movies?search=The&skip=3&limit=3")

        assert response1.status_code == 200
        assert response2.status_code == 200

        movies1 = response1.json()
        movies2 = response2.json()

        # Results should be different if there are enough matches
        if len(movies1) == 3 and len(movies2) > 0:
            assert movies1[0]["id"] != movies2[0]["id"]

    def test_pagination_consistency(self):
        """Test pagination returns consistent results."""
        # Get first page
        response1 = client.get("/api/movies?limit=5")
        movies1 = response1.json()

        # Get same page again
        response2 = client.get("/api/movies?limit=5")
        movies2 = response2.json()

        # Should be identical
        assert len(movies1) == len(movies2)
        if len(movies1) > 0:
            assert movies1[0]["id"] == movies2[0]["id"]


class TestSorting:
    """Test result ordering and sorting."""

    def test_movies_have_consistent_order(self):
        """Test movies are returned in consistent order."""
        response1 = client.get("/api/movies")
        response2 = client.get("/api/movies")

        movies1 = response1.json()
        movies2 = response2.json()

        # Order should be consistent
        assert len(movies1) == len(movies2)
        if len(movies1) > 0:
            assert movies1[0]["id"] == movies2[0]["id"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
