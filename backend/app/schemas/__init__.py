from .genre import Genre, GenreCreate, GenreUpdate
from .rating import Rating, RatingCreate, RatingUpdate
from .director import Director, DirectorCreate, DirectorUpdate, DirectorDetail
from .actor import Actor, ActorCreate, ActorUpdate, ActorDetail
from .movie import Movie, MovieCreate, MovieUpdate, MovieDetail

# Rebuild models to resolve forward references
ActorDetail.model_rebuild()
DirectorDetail.model_rebuild()
MovieDetail.model_rebuild()

__all__ = [
    "Movie", "MovieCreate", "MovieUpdate", "MovieDetail",
    "Actor", "ActorCreate", "ActorUpdate", "ActorDetail",
    "Director", "DirectorCreate", "DirectorUpdate", "DirectorDetail",
    "Genre", "GenreCreate", "GenreUpdate",
    "Rating", "RatingCreate", "RatingUpdate",
]
