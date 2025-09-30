from sqlalchemy.orm import Session
from app.models import Movie, Actor, Director, Genre, Rating


def seed_database(db: Session):
    """Populate database with sample movie data."""
    
    # Check if data already exists
    if db.query(Movie).first():
        print("Database already seeded. Skipping...")
        return

    # Create Genres
    genres_data = [
        Genre(name="Action"),
        Genre(name="Drama"),
        Genre(name="Comedy"),
        Genre(name="Sci-Fi"),
        Genre(name="Thriller"),
        Genre(name="Romance"),
        Genre(name="Crime"),
        Genre(name="Fantasy"),
        Genre(name="Horror"),
        Genre(name="Adventure"),
    ]
    db.add_all(genres_data)
    db.commit()

    # Create Directors
    directors_data = [
        Director(name="Christopher Nolan", bio="British-American filmmaker known for complex narratives.", photo_url="https://image.tmdb.org/t/p/w500/5xU17nQuj9aB9GoopdfSX0QgTqG.jpg"),
        Director(name="Quentin Tarantino", bio="American filmmaker known for nonlinear storylines.", photo_url="https://image.tmdb.org/t/p/w500/8jEumAVtJ4BXZgqDkJ4e6q1cY1l.jpg"),
        Director(name="Martin Scorsese", bio="Legendary American director and film historian.", photo_url="https://image.tmdb.org/t/p/w500/9U9Y5GQuWX3EZy39B8nkk4NY01S.jpg"),
        Director(name="Steven Spielberg", bio="One of the founding pioneers of the New Hollywood era.", photo_url="https://image.tmdb.org/t/p/w500/7xXJ15VEf7G9GdAuV1dOdcPw4hP.jpg"),
        Director(name="Denis Villeneuve", bio="Canadian filmmaker known for ambitious sci-fi films.", photo_url="https://image.tmdb.org/t/p/w500/5U8BHbGC5ocBphl58tb3Vb9V0EA.jpg"),
        Director(name="Greta Gerwig", bio="American actress and filmmaker.", photo_url="https://image.tmdb.org/t/p/w500/8kOGNJBR9X2V7XvO7i3hX2kF5yL.jpg"),
        Director(name="Jordan Peele", bio="American filmmaker known for social thriller films.", photo_url="https://image.tmdb.org/t/p/w500/6J7fXIGqjqjqjqjqjqjqjqjqjqjq.jpg"),
        Director(name="Bong Joon-ho", bio="South Korean filmmaker known for genre-bending films.", photo_url="https://image.tmdb.org/t/p/w500/5U8BHbGC5ocBphl58tb3Vb9V0EA.jpg"),
    ]
    db.add_all(directors_data)
    db.commit()

    # Create Actors
    actors_data = [
        Actor(name="Leonardo DiCaprio", bio="American actor and film producer.", photo_url="https://image.tmdb.org/t/p/w500/5Brc5dLifH3suIax9hsWg2Uq4O.jpg"),
        Actor(name="Christian Bale", bio="English actor known for method acting.", photo_url="https://image.tmdb.org/t/p/w500/qCpZn2e3dimwbryLnqxZuQ88st.jpg"),
        Actor(name="Samuel L. Jackson", bio="American actor and producer.", photo_url="https://image.tmdb.org/t/p/w500/5Brc5dLifH3suIax9hsWg2Uq4O.jpg"),
        Actor(name="Morgan Freeman", bio="American actor, director, and narrator.", photo_url="https://image.tmdb.org/t/p/w500/oGJQhOpT8S1M56tvSsbEBePV5O1.jpg"),
        Actor(name="Robert De Niro", bio="American actor and producer.", photo_url="https://image.tmdb.org/t/p/w500/8Bgdfv1oN9Mw0YuMHP6fw8KzDkc.jpg"),
        Actor(name="Tom Hanks", bio="American actor and filmmaker.", photo_url="https://image.tmdb.org/t/p/w500/xndWFs6Ckd7jkqD6z3i5a98wS3v.jpg"),
        Actor(name="Scarlett Johansson", bio="American actress and singer.", photo_url="https://image.tmdb.org/t/p/w500/6NsMbJXRlDZuDzatN2akFdGuTvx.jpg"),
        Actor(name="Brad Pitt", bio="American actor and film producer.", photo_url="https://image.tmdb.org/t/p/w500/cckcYc2v0yh1tc9QjKrptksfizC.jpg"),
        Actor(name="Cillian Murphy", bio="Irish actor known for intense performances.", photo_url="https://image.tmdb.org/t/p/w500/2v9FVVBUrrkW2m3QOcYkuhq9A6o.jpg"),
        Actor(name="Margot Robbie", bio="Australian actress and producer.", photo_url="https://image.tmdb.org/t/p/w500/euDPyqLnuwaWMHajcU3oZ9uZezR.jpg"),
        Actor(name="Ryan Gosling", bio="Canadian actor and musician.", photo_url="https://image.tmdb.org/t/p/w500/4EuJ0o59ipS4k5t8Wb8igI9Mx6b.jpg"),
        Actor(name="Timothée Chalamet", bio="American and French actor.", photo_url="https://image.tmdb.org/t/p/w500/8xV47e7Rudb96lcyvnLJ3y8bYS.jpg"),
        Actor(name="Zendaya", bio="American actress and singer.", photo_url="https://image.tmdb.org/t/p/w500/6TE2AlGWqc4uJjH7e4xjq6dUxCW.jpg"),
        Actor(name="Daniel Kaluuya", bio="British actor and writer.", photo_url="https://image.tmdb.org/t/p/w500/4EuJ0o59ipS4k5t8Wb8igI9Mx6b.jpg"),
        Actor(name="Song Kang-ho", bio="South Korean actor.", photo_url="https://image.tmdb.org/t/p/w500/5Brc5dLifH3suIax9hsWg2Uq4O.jpg"),
    ]
    db.add_all(actors_data)
    db.commit()

    # Helper to get objects by name
    def get_genre(name): return db.query(Genre).filter(Genre.name == name).first()
    def get_director(name): return db.query(Director).filter(Director.name == name).first()
    def get_actor(name): return db.query(Actor).filter(Actor.name == name).first()

    # Create Movies with relationships
    movies_data = [
        {
            "movie": Movie(
                title="Inception",
                release_year=2010,
                synopsis="A thief who steals corporate secrets through dream-sharing technology.",
                poster_url="https://image.tmdb.org/t/p/w500/9gk7adHYeDvHkCSEqAvQNLV5Uge.jpg",
                duration_minutes=148,
                status="Released",
                director=get_director("Christopher Nolan")
            ),
            "genres": ["Sci-Fi", "Action", "Thriller"],
            "actors": ["Leonardo DiCaprio", "Cillian Murphy"],
            "ratings": [
                Rating(score=8.8, review="Mind-bending masterpiece with stunning visuals."),
                Rating(score=9.0, review="Nolan's best work. Complex but rewarding."),
            ]
        },
        {
            "movie": Movie(
                title="The Dark Knight",
                release_year=2008,
                synopsis="Batman faces the Joker, a criminal mastermind who wants to plunge Gotham into anarchy.",
                poster_url="https://image.tmdb.org/t/p/w500/qJ2tW6WMUDux911r6m7haRef0WH.jpg",
                duration_minutes=152,
                status="Released",
                director=get_director("Christopher Nolan")
            ),
            "genres": ["Action", "Crime", "Drama"],
            "actors": ["Christian Bale", "Morgan Freeman"],
            "ratings": [
                Rating(score=9.0, review="The greatest superhero movie ever made."),
                Rating(score=8.9, review="Heath Ledger's Joker is legendary."),
            ]
        },
        {
            "movie": Movie(
                title="Pulp Fiction",
                release_year=1994,
                synopsis="The lives of two mob hitmen, a boxer, and a pair of diner bandits intertwine.",
                poster_url="https://image.tmdb.org/t/p/w500/d5iIlFn5s0ImszYzBPb8JPIfbXD.jpg",
                duration_minutes=154,
                status="Released",
                director=get_director("Quentin Tarantino")
            ),
            "genres": ["Crime", "Drama"],
            "actors": ["Samuel L. Jackson", "Brad Pitt"],
            "ratings": [
                Rating(score=8.9, review="Revolutionary storytelling and unforgettable dialogue."),
            ]
        },
        {
            "movie": Movie(
                title="The Shawshank Redemption",
                release_year=1994,
                synopsis="Two imprisoned men bond over years, finding redemption through acts of decency.",
                poster_url="https://image.tmdb.org/t/p/w500/q6y0Go1tsGEsmtFryDOJo3dEmqu.jpg",
                duration_minutes=142,
                status="Released",
                director=get_director("Steven Spielberg")
            ),
            "genres": ["Drama"],
            "actors": ["Morgan Freeman", "Brad Pitt"],
            "ratings": [
                Rating(score=9.3, review="The most inspiring film ever made."),
                Rating(score=9.2, review="Perfect in every way."),
            ]
        },
        {
            "movie": Movie(
                title="Goodfellas",
                release_year=1990,
                synopsis="The story of Henry Hill and his life in the mob.",
                poster_url="https://image.tmdb.org/t/p/w500/aKuFiU82s5ISJpGZp7YkIr3kCUd.jpg",
                duration_minutes=146,
                status="Released",
                director=get_director("Martin Scorsese")
            ),
            "genres": ["Crime", "Drama"],
            "actors": ["Robert De Niro", "Samuel L. Jackson"],
            "ratings": [
                Rating(score=8.7, review="Scorsese's crime masterpiece."),
            ]
        },
        {
            "movie": Movie(
                title="Saving Private Ryan",
                release_year=1998,
                synopsis="Following the Normandy Landings, a group of soldiers search for a paratrooper.",
                poster_url="https://image.tmdb.org/t/p/w500/uqx37cS8cpHg8U35f9U5IBlrCV3.jpg",
                duration_minutes=169,
                status="Released",
                director=get_director("Steven Spielberg")
            ),
            "genres": ["Drama", "Action"],
            "actors": ["Tom Hanks"],
            "ratings": [
                Rating(score=8.6, review="The most realistic war film ever created."),
            ]
        },
        {
            "movie": Movie(
                title="Dune",
                release_year=2021,
                synopsis="Paul Atreides journeys to the dangerous planet Arrakis to ensure his family's future.",
                poster_url="https://image.tmdb.org/t/p/w500/d5NXSklXo0qyIYkgV94XAgMIckC.jpg",
                duration_minutes=155,
                status="Released",
                director=get_director("Denis Villeneuve")
            ),
            "genres": ["Sci-Fi", "Adventure"],
            "actors": ["Timothée Chalamet", "Zendaya"],
            "ratings": [
                Rating(score=8.0, review="Visually stunning epic sci-fi."),
                Rating(score=8.2, review="A triumph of world-building."),
            ]
        },
        {
            "movie": Movie(
                title="Barbie",
                release_year=2023,
                synopsis="Barbie and Ken explore the real world and discover their true selves.",
                poster_url="https://image.tmdb.org/t/p/w500/iuFNMS8U5cb6xfzi51Dbkovj7vM.jpg",
                duration_minutes=114,
                status="Released",
                director=get_director("Greta Gerwig")
            ),
            "genres": ["Comedy", "Adventure", "Fantasy"],
            "actors": ["Margot Robbie", "Ryan Gosling"],
            "ratings": [
                Rating(score=7.4, review="Surprisingly deep and incredibly fun."),
            ]
        },
        {
            "movie": Movie(
                title="Oppenheimer",
                release_year=2023,
                synopsis="The story of J. Robert Oppenheimer and the development of the atomic bomb.",
                poster_url="https://image.tmdb.org/t/p/w500/8Gxv8gSFCU0XGDykEGv7zR1n2ua.jpg",
                duration_minutes=180,
                status="Released",
                director=get_director("Christopher Nolan")
            ),
            "genres": ["Drama", "Thriller"],
            "actors": ["Cillian Murphy", "Robert De Niro"],
            "ratings": [
                Rating(score=8.5, review="Nolan's most mature and powerful film."),
                Rating(score=8.7, review="Cillian Murphy delivers a career-defining performance."),
            ]
        },
        {
            "movie": Movie(
                title="Get Out",
                release_year=2017,
                synopsis="A young Black man visits his white girlfriend's family estate.",
                poster_url="https://image.tmdb.org/t/p/w500/tFXcEccSQMf3lfhfXKSU9iRBpa3.jpg",
                duration_minutes=104,
                status="Released",
                director=get_director("Jordan Peele")
            ),
            "genres": ["Horror", "Thriller"],
            "actors": ["Daniel Kaluuya"],
            "ratings": [
                Rating(score=7.7, review="Smart social commentary wrapped in horror."),
            ]
        },
        {
            "movie": Movie(
                title="Parasite",
                release_year=2019,
                synopsis="A poor family schemes to become employed by a wealthy family.",
                poster_url="https://image.tmdb.org/t/p/w500/7IiTTgloJzvGI1TAYymCfbfl3vT.jpg",
                duration_minutes=132,
                status="Released",
                director=get_director("Bong Joon-ho")
            ),
            "genres": ["Drama", "Thriller"],
            "actors": ["Song Kang-ho"],
            "ratings": [
                Rating(score=8.6, review="A genre-defying masterpiece."),
                Rating(score=8.9, review="Unpredictable and unforgettable."),
            ]
        },
        {
            "movie": Movie(
                title="The Wolf of Wall Street",
                release_year=2013,
                synopsis="The story of Jordan Belfort's rise and fall on Wall Street.",
                poster_url="https://image.tmdb.org/t/p/w500/34m2tygAYBGqA9MXKhRDtzYd4MR.jpg",
                duration_minutes=180,
                status="Released",
                director=get_director("Martin Scorsese")
            ),
            "genres": ["Crime", "Comedy", "Drama"],
            "actors": ["Leonardo DiCaprio", "Margot Robbie"],
            "ratings": [
                Rating(score=8.2, review="Excessive, outrageous, and entertaining."),
            ]
        },
        {
            "movie": Movie(
                title="Fight Club",
                release_year=1999,
                synopsis="An insomniac office worker forms an underground fight club.",
                poster_url="https://image.tmdb.org/t/p/w500/pB8BM7pdSp6B6Ih7QZ4DrQ3PmJK.jpg",
                duration_minutes=139,
                status="Released",
                director=get_director("Steven Spielberg")
            ),
            "genres": ["Drama", "Thriller"],
            "actors": ["Brad Pitt"],
            "ratings": [
                Rating(score=8.8, review="Subversive and unforgettable."),
            ]
        },
    ]

    # Add movies with their relationships
    for item in movies_data:
        movie = item["movie"]
        
        # Add genres
        for genre_name in item["genres"]:
            genre = get_genre(genre_name)
            if genre:
                movie.genres.append(genre)
        
        # Add actors
        for actor_name in item["actors"]:
            actor = get_actor(actor_name)
            if actor:
                movie.actors.append(actor)
        
        # Add ratings
        for rating in item["ratings"]:
            movie.ratings.append(rating)
        
        db.add(movie)
    
    db.commit()
    print("Database seeded successfully with sample data!")
