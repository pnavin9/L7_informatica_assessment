"""Test Pydantic schemas validation."""
import pytest
from pydantic import ValidationError
from app.schemas import RatingCreate, MovieCreate, GenreCreate, ActorCreate


def test_rating_score_validation():
    """Test rating score is validated between 0.0 and 10.0."""
    
    # Valid scores
    valid = RatingCreate(movie_id=1, score=8.5, review="Great movie!")
    assert valid.score == 8.5
    
    valid_min = RatingCreate(movie_id=1, score=0.0)
    assert valid_min.score == 0.0
    
    valid_max = RatingCreate(movie_id=1, score=10.0)
    assert valid_max.score == 10.0
    
    # Invalid: score too low
    with pytest.raises(ValidationError) as exc:
        RatingCreate(movie_id=1, score=-1.0)
    assert "greater than or equal to 0" in str(exc.value)
    
    # Invalid: score too high
    with pytest.raises(ValidationError) as exc:
        RatingCreate(movie_id=1, score=11.0)
    assert "less than or equal to 10" in str(exc.value)


def test_movie_year_validation():
    """Test movie release year validation."""
    
    # Valid year
    valid = MovieCreate(
        title="Inception",
        release_year=2010,
        director_id=1
    )
    assert valid.release_year == 2010
    
    # Invalid: year too early
    with pytest.raises(ValidationError) as exc:
        MovieCreate(title="Test", release_year=1800, director_id=1)
    assert "1888" in str(exc.value)
    
    # Invalid: year too late
    with pytest.raises(ValidationError) as exc:
        MovieCreate(title="Test", release_year=2200, director_id=1)
    assert "2100" in str(exc.value)


def test_required_fields():
    """Test required field validation."""
    
    # Missing title
    with pytest.raises(ValidationError):
        MovieCreate(release_year=2010, director_id=1)
    
    # Missing score
    with pytest.raises(ValidationError):
        RatingCreate(movie_id=1)
    
    # Missing name
    with pytest.raises(ValidationError):
        GenreCreate()


def test_string_length_validation():
    """Test string length constraints."""
    
    # Valid lengths
    actor = ActorCreate(name="Tom Hanks", bio="American actor")
    assert actor.name == "Tom Hanks"
    
    # Empty name not allowed
    with pytest.raises(ValidationError) as exc:
        ActorCreate(name="")
    assert "at least 1 character" in str(exc.value)
    
    # Name too long (over 255 chars)
    with pytest.raises(ValidationError):
        ActorCreate(name="X" * 300)


def test_optional_fields():
    """Test optional fields work correctly."""
    
    # Review is optional
    rating = RatingCreate(movie_id=1, score=8.0)
    assert rating.review is None
    
    # Bio is optional
    actor = ActorCreate(name="Test Actor")
    assert actor.bio is None
    
    # Synopsis is optional
    movie = MovieCreate(title="Test", release_year=2020, director_id=1)
    assert movie.synopsis is None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
