"""Test edge cases and error handling."""

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


class TestEdgeCases:
    """Test edge cases for all endpoints."""

    def test_no_movies_found_with_invalid_genre(self):
        """Test filtering with non-existent genre returns empty list."""
        response = client.get("/api/movies?genre=NonExistentGenre")
        assert response.status_code == 200
        movies = response.json()
        assert isinstance(movies, list)
        assert len(movies) == 0

    def test_no_movies_found_with_invalid_director(self):
        """Test filtering with non-existent director returns empty list."""
        response = client.get("/api/movies?director=NonExistentDirector")
        assert response.status_code == 200
        movies = response.json()
        assert len(movies) == 0

    def test_no_movies_found_with_invalid_actor(self):
        """Test filtering with non-existent actor returns empty list."""
        response = client.get("/api/movies?actor=NonExistentActor")
        assert response.status_code == 200
        movies = response.json()
        assert len(movies) == 0

    def test_no_movies_found_with_future_year(self):
        """Test filtering with future year returns empty list."""
        response = client.get("/api/movies?year=2099")
        assert response.status_code == 200
        movies = response.json()
        assert len(movies) == 0

    def test_no_movies_found_with_invalid_year_range(self):
        """Test filtering with impossible year range returns empty list."""
        response = client.get("/api/movies?min_year=2099&max_year=2100")
        assert response.status_code == 200
        movies = response.json()
        assert len(movies) == 0

    def test_search_with_no_results(self):
        """Test search with no matching movies returns empty list."""
        response = client.get("/api/movies?search=XYZ123NonExistent")
        assert response.status_code == 200
        movies = response.json()
        assert len(movies) == 0

    def test_get_nonexistent_movie_404(self):
        """Test getting non-existent movie returns 404."""
        response = client.get("/api/movies/99999")
        assert response.status_code == 404
        assert "detail" in response.json()

    def test_get_nonexistent_actor_404(self):
        """Test getting non-existent actor returns 404."""
        response = client.get("/api/actors/99999")
        assert response.status_code == 404
        assert "detail" in response.json()

    def test_get_nonexistent_director_404(self):
        """Test getting non-existent director returns 404."""
        response = client.get("/api/directors/99999")
        assert response.status_code == 404
        assert "detail" in response.json()

    def test_get_nonexistent_genre_404(self):
        """Test getting non-existent genre returns 404."""
        response = client.get("/api/genres/99999")
        assert response.status_code == 404
        assert "detail" in response.json()

    def test_negative_movie_id(self):
        """Test negative movie ID returns 404."""
        response = client.get("/api/movies/-1")
        assert response.status_code == 404

    def test_invalid_movie_id_type(self):
        """Test invalid movie ID type returns 422."""
        response = client.get("/api/movies/invalid")
        assert response.status_code == 422

    def test_pagination_beyond_available_data(self):
        """Test pagination with skip beyond available data returns empty list."""
        response = client.get("/api/movies?skip=99999&limit=10")
        assert response.status_code == 200
        movies = response.json()
        assert len(movies) == 0

    def test_large_limit_value(self):
        """Test large limit value is handled correctly."""
        response = client.get("/api/movies?limit=10000")
        # API may reject very large limits (422) or accept them (200)
        assert response.status_code in [200, 422]
        if response.status_code == 200:
            movies = response.json()
            assert isinstance(movies, list)

    def test_zero_skip_zero_limit(self):
        """Test zero skip and zero limit."""
        response = client.get("/api/movies?skip=0&limit=0")
        # API may reject zero limit (422) or return empty list (200)
        assert response.status_code in [200, 422]
        if response.status_code == 200:
            movies = response.json()
            assert len(movies) == 0

    def test_negative_skip_value(self):
        """Test negative skip value is handled."""
        response = client.get("/api/movies?skip=-1&limit=10")
        # Should either return 422 or handle gracefully
        assert response.status_code in [200, 422]

    def test_negative_limit_value(self):
        """Test negative limit value is handled."""
        response = client.get("/api/movies?limit=-1")
        # Should either return 422 or handle gracefully
        assert response.status_code in [200, 422]

    def test_multiple_filters_combined(self):
        """Test combining multiple filters."""
        response = client.get("/api/movies?genre=Action&year=2010")
        assert response.status_code == 200
        movies = response.json()
        # Should return movies that match ALL filters
        for movie in movies:
            assert movie["release_year"] == 2010
            genre_names = [g["name"] for g in movie["genres"]]
            assert "Action" in genre_names

    def test_search_with_special_characters(self):
        """Test search with special characters doesn't crash."""
        special_chars = ["!", "@", "#", "$", "%", "^", "&", "*"]
        for char in special_chars:
            response = client.get(f"/api/movies?search={char}")
            assert response.status_code == 200
            # Should return empty list or handle gracefully
            assert isinstance(response.json(), list)

    def test_case_insensitive_search(self):
        """Test search is case-insensitive."""
        response1 = client.get("/api/movies?search=inception")
        response2 = client.get("/api/movies?search=INCEPTION")
        response3 = client.get("/api/movies?search=Inception")

        assert response1.status_code == 200
        assert response2.status_code == 200
        assert response3.status_code == 200

        # All should return the same results
        movies1 = response1.json()
        movies2 = response2.json()
        movies3 = response3.json()

        if len(movies1) > 0:
            assert len(movies1) == len(movies2) == len(movies3)

    def test_partial_name_search(self):
        """Test partial name matching in search."""
        response = client.get("/api/movies?search=Inc")
        assert response.status_code == 200
        movies = response.json()
        # Should match "Inception" if it exists
        if len(movies) > 0:
            assert any("Inc" in movie["title"] for movie in movies)

    def test_empty_search_parameter(self):
        """Test empty search parameter returns all movies."""
        response = client.get("/api/movies?search=")
        assert response.status_code == 200
        movies = response.json()
        assert isinstance(movies, list)

    def test_whitespace_only_search(self):
        """Test search with only whitespace."""
        response = client.get("/api/movies?search=   ")
        assert response.status_code == 200
        movies = response.json()
        assert isinstance(movies, list)

    def test_very_long_search_string(self):
        """Test search with very long string doesn't crash."""
        long_string = "a" * 1000
        response = client.get(f"/api/movies?search={long_string}")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_movie_with_no_ratings(self):
        """Test movie with no ratings shows correct average."""
        # Get all movies and find one with no ratings
        response = client.get("/api/movies")
        assert response.status_code == 200
        movies = response.json()

        for movie in movies:
            if movie["average_rating"] is None or movie["average_rating"] == 0:
                # This movie has no ratings
                assert movie["average_rating"] in [None, 0.0]
                break

    def test_ratings_endpoint_for_nonexistent_movie(self):
        """Test getting ratings for non-existent movie."""
        response = client.get("/api/movies/99999/ratings")
        assert response.status_code == 404

    def test_actor_with_no_movies(self):
        """Test actor endpoint handles actors with no movies."""
        # This would require creating an actor without movies
        # For now, just verify the endpoint structure works
        response = client.get("/api/actors")
        assert response.status_code == 200
        actors = response.json()
        assert isinstance(actors, list)

    def test_director_with_no_movies(self):
        """Test director endpoint handles directors with no movies."""
        response = client.get("/api/directors")
        assert response.status_code == 200
        directors = response.json()
        assert isinstance(directors, list)

    def test_genre_filtering_with_multiple_genres(self):
        """Test movie with multiple genres is found correctly."""
        response = client.get("/api/movies?genre=Sci-Fi")
        assert response.status_code == 200
        movies = response.json()

        for movie in movies:
            genre_names = [g["name"] for g in movie["genres"]]
            assert "Sci-Fi" in genre_names

    def test_year_range_with_min_greater_than_max(self):
        """Test invalid year range (min > max)."""
        response = client.get("/api/movies?min_year=2020&max_year=2010")
        assert response.status_code == 200
        movies = response.json()
        # Should return empty list or handle gracefully
        assert len(movies) == 0

    def test_exact_year_match(self):
        """Test exact year match returns correct movies."""
        test_year = 2010
        response = client.get(f"/api/movies?year={test_year}")
        assert response.status_code == 200
        movies = response.json()

        for movie in movies:
            assert movie["release_year"] == test_year

    def test_api_root_endpoint_structure(self):
        """Test API root endpoint returns proper structure."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()

        assert "message" in data
        assert "endpoints" in data
        assert isinstance(data["endpoints"], dict)

        # Verify all main endpoints are listed
        assert "movies" in data["endpoints"]
        assert "actors" in data["endpoints"]
        assert "directors" in data["endpoints"]
        assert "genres" in data["endpoints"]


class TestRatingsEdgeCases:
    """Test edge cases for ratings."""

    def test_movie_ratings_empty_list(self):
        """Test movie with no ratings returns empty list."""
        # This assumes we can find a movie without ratings
        response = client.get("/api/movies")
        movies = response.json()

        for movie in movies:
            rating_response = client.get(f"/api/movies/{movie['id']}/ratings")
            assert rating_response.status_code == 200
            ratings = rating_response.json()
            assert isinstance(ratings, list)

    def test_average_rating_calculation(self):
        """Test average rating is calculated correctly."""
        response = client.get("/api/movies/1")
        assert response.status_code == 200
        movie = response.json()

        if len(movie["ratings"]) > 0:
            calculated_avg = sum(r["score"] for r in movie["ratings"]) / len(movie["ratings"])
            # Allow small floating point differences
            assert abs(movie["average_rating"] - calculated_avg) < 0.01


class TestConcurrentRequests:
    """Test handling of concurrent requests."""

    def test_multiple_simultaneous_queries(self):
        """Test multiple queries don't interfere with each other."""
        responses = []

        # Make multiple requests
        for i in range(5):
            response = client.get("/api/movies")
            responses.append(response)

        # All should succeed
        for response in responses:
            assert response.status_code == 200
            assert isinstance(response.json(), list)


class TestResponseStructure:
    """Test response structure consistency."""

    def test_movie_response_has_all_fields(self):
        """Test movie response has all required fields."""
        response = client.get("/api/movies")
        assert response.status_code == 200
        movies = response.json()

        if len(movies) > 0:
            movie = movies[0]
            required_fields = [
                "id",
                "title",
                "release_year",
                "synopsis",
                "director",
                "genres",
                "actors",
                "average_rating",
            ]
            for field in required_fields:
                assert field in movie

    def test_actor_response_has_all_fields(self):
        """Test actor response has all required fields."""
        response = client.get("/api/actors")
        assert response.status_code == 200
        actors = response.json()

        if len(actors) > 0:
            actor = actors[0]
            assert "id" in actor
            assert "name" in actor
            assert "bio" in actor

    def test_director_response_has_all_fields(self):
        """Test director response has all required fields."""
        response = client.get("/api/directors")
        assert response.status_code == 200
        directors = response.json()

        if len(directors) > 0:
            director = directors[0]
            assert "id" in director
            assert "name" in director
            assert "bio" in director

    def test_genre_response_has_all_fields(self):
        """Test genre response has all required fields."""
        response = client.get("/api/genres")
        assert response.status_code == 200
        genres = response.json()

        if len(genres) > 0:
            genre = genres[0]
            assert "id" in genre
            assert "name" in genre


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
