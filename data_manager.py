from models import db, User, Movie

class DataManager:

    # -------------------------
    # USER CRUD
    # -------------------------

    def create_user(self, name):
        """Create a new user."""
        new_user = User(name=name)
        db.session.add(new_user)
        db.session.commit()
        return new_user

    def get_users(self):
        """Return all users."""
        return User.query.all()

    # -------------------------
    # MOVIE CRUD
    # -------------------------

    def get_movies(self, user_id):
        """Return all movies for a specific user."""
        return Movie.query.filter_by(user_id=user_id).all()

    def add_movie(self, movie):
        """
        Add a new movie.
        movie must be a Movie object already containing:
        name, director, year, poster_url, user_id
        """
        db.session.add(movie)
        db.session.commit()
        return movie

    def update_movie(self, movie_id, new_title):
        """Update the title of a movie."""
        movie = Movie.query.get(movie_id)
        if movie:
            movie.name = new_title
            db.session.commit()
        return movie

    def delete_movie(self, movie_id):
        """Delete a movie."""
        movie = Movie.query.get(movie_id)
        if movie:
            db.session.delete(movie)
            db.session.commit()
        return movie
