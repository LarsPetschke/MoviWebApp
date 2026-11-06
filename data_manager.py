from sqlalchemy import func
from models import db, User, Movie

class DataManager:

    # -------------------------
    # USER CRUD
    # -------------------------

    def create_user(self, name):
        try:
            new_user = User(name=name)
            db.session.add(new_user)
            db.session.commit()
            return new_user
        except Exception as e:
            db.session.rollback()
            print("Fehler beim Erstellen eines Nutzers:", str(e))
            return None

    def get_users(self):
        """Return all users."""
        return User.query.all()

    def get_user(self, user_id):
        """Return a single user or None."""
        return db.session.get(User, user_id)

    # -------------------------
    # MOVIE CRUD
    # -------------------------

    def get_movies(self, user_id):
        """Return all movies for a specific user."""
        return Movie.query.filter_by(user_id=user_id).all()

    def find_movie(self, title, year):
        """Search all movies for title (case-insensitive) + year with a known director."""
        return Movie.query.filter(
            func.lower(Movie.name) == title.lower(),
            Movie.year == year,
            Movie.director != "Unknown",
            Movie.director != ""
        ).first()

    def add_movie(self, movie):
        """
        Add a new movie.
        movie must be a Movie object already containing:
        name, director, year, poster_url, user_id
        """
        db.session.add(movie)
        db.session.commit()
        return movie

    def update_movie(self, movie_id, new_title=None, new_year=None):
        """Update title and/or year of a movie (None = unchanged)."""
        movie = Movie.query.get(movie_id)
        if movie:
            if new_title:
                movie.name = new_title
            if new_year is not None:
                movie.year = new_year
            db.session.commit()
        return movie

    def delete_movie(self, movie_id):
        """Delete a movie."""
        movie = Movie.query.get(movie_id)
        if movie:
            db.session.delete(movie)
            db.session.commit()
        return movie
