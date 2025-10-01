from .actor import Actor, ActorCreate, ActorDetail, ActorUpdate
from .director import Director, DirectorCreate, DirectorDetail, DirectorUpdate
from .genre import Genre, GenreCreate, GenreUpdate
from .movie import Movie, MovieCreate, MovieDetail, MovieUpdate
from .rating import Rating, RatingCreate, RatingUpdate

# Rebuild models to resolve forward references
ActorDetail.model_rebuild()
DirectorDetail.model_rebuild()
MovieDetail.model_rebuild()

__all__ = [
    "Movie",
    "MovieCreate",
    "MovieUpdate",
    "MovieDetail",
    "Actor",
    "ActorCreate",
    "ActorUpdate",
    "ActorDetail",
    "Director",
    "DirectorCreate",
    "DirectorUpdate",
    "DirectorDetail",
    "Genre",
    "GenreCreate",
    "GenreUpdate",
    "Rating",
    "RatingCreate",
    "RatingUpdate",
]
