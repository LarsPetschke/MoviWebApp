from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    # Beziehung: Ein User → viele Movies
    movies = db.relationship('Movie', backref='user', lazy=True)


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    director = db.Column(db.String(200), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    poster_url = db.Column(db.String(500))

    # Foreign Key → jeder Film gehört zu genau einem User
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
