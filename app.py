from flask import Flask, request, redirect, url_for
from data_manager import DataManager
from models import db, Movie
import os

app = Flask(__name__)

# SQLAlchemy konfigurieren
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/movies.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Datenbank mit der App verknüpfen
db.init_app(app)

# DataManager erstellen
data_manager = DataManager()


# ---------------------------------------------------------
# Startseite: Nutzer anzeigen (GET)
# ---------------------------------------------------------
@app.route('/')
def home():
    users = data_manager.get_users()
    return str(users)   # später ersetzen wir das durch Templates


# ---------------------------------------------------------
# Nutzer hinzufügen (POST)
# ---------------------------------------------------------
@app.route('/users', methods=['POST'])
def add_user():
    name = request.form.get('name')
    if name:
        data_manager.create_user(name)
    return redirect(url_for('home'))


# ---------------------------------------------------------
# Filme eines Nutzers anzeigen (GET)
# ---------------------------------------------------------
@app.route('/users/<int:user_id>/movies', methods=['GET'])
def list_movies(user_id):
    movies = data_manager.get_movies(user_id)
    return str(movies)   # später ersetzen wir das durch Templates


# ---------------------------------------------------------
# Film hinzufügen (POST)
# ---------------------------------------------------------
@app.route('/users/<int:user_id>/movies', methods=['POST'])
def add_movie(user_id):
    title = request.form.get('title')

    # OMDb-Integration kommt später
    movie = Movie(
        name=title,
        director="Unknown",
        year=0,
        poster_url="",
        user_id=user_id
    )

    data_manager.add_movie(movie)
    return redirect(url_for('list_movies', user_id=user_id))


# ---------------------------------------------------------
# Film aktualisieren (POST)
# ---------------------------------------------------------
@app.route('/users/<int:user_id>/movies/<int:movie_id>/update', methods=['POST'])
def update_movie(user_id, movie_id):
    new_title = request.form.get('new_title')
    data_manager.update_movie(movie_id, new_title)
    return redirect(url_for('list_movies', user_id=user_id))


# ---------------------------------------------------------
# Film löschen (POST)
# ---------------------------------------------------------
@app.route('/users/<int:user_id>/movies/<int:movie_id>/delete', methods=['POST'])
def delete_movie(user_id, movie_id):
    data_manager.delete_movie(movie_id)
    return redirect(url_for('list_movies', user_id=user_id))


# ---------------------------------------------------------
# App starten + Datenbank erzeugen
# ---------------------------------------------------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()from flask import Flask, request, redirect, url_for, render_template
from data_manager import DataManager
from models import db, Movie
import os

app = Flask(__name__)

# Codio-Datenbank im instance/-Ordner
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///instance/movies.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Datenbank mit der App verknüpfen
db.init_app(app)

# DataManager erstellen
data_manager = DataManager()


# ---------------------------------------------------------
# Startseite: Nutzer anzeigen (GET)
# ---------------------------------------------------------
@app.route('/')
def index():
    users = data_manager.get_users()
    return render_template('index.html', users=users)


# ---------------------------------------------------------
# Nutzer hinzufügen (POST)
# ---------------------------------------------------------
@app.route('/users', methods=['POST'])
def create_user():
    name = request.form.get('name')
    if name:
        data_manager.create_user(name)
    return redirect(url_for('index'))


# ---------------------------------------------------------
# Filme eines Nutzers anzeigen (GET)
# ---------------------------------------------------------
@app.route('/users/<int:user_id>/movies', methods=['GET'])
def get_movies(user_id):
    movies = data_manager.get_movies(user_id)
    return render_template('movies.html', movies=movies, user_id=user_id)


# ---------------------------------------------------------
# Film hinzufügen (POST)
# ---------------------------------------------------------
@app.route('/users/<int:user_id>/movies', methods=['POST'])
def add_movie(user_id):
    title = request.form.get('title')

    # OMDb-Integration kommt später
    movie = Movie(
        name=title,
        director="Unknown",
        year=0,
        poster_url="",
        user_id=user_id
    )

    data_manager.add_movie(movie)
    return redirect(url_for('get_movies', user_id=user_id))


# ---------------------------------------------------------
# Film aktualisieren (POST)
# ---------------------------------------------------------
@app.route('/users/<int:user_id>/movies/<int:movie_id>/update', methods=['POST'])
def update_movie(user_id, movie_id):
    new_title = request.form.get('new_title')
    data_manager.update_movie(movie_id, new_title)
    return redirect(url_for('get_movies', user_id=user_id))


# ---------------------------------------------------------
# Film löschen (POST)
# ---------------------------------------------------------
@app.route('/users/<int:user_id>/movies/<int:movie_id>/delete', methods=['POST'])
def delete_movie(user_id, movie_id):
    data_manager.delete_movie(movie_id)
    return redirect(url_for('get_movies', user_id=user_id))


# ---------------------------------------------------------
# Fehlerbehandlung (POST)
# ---------------------------------------------------------
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


# ---------------------------------------------------------
# App starten + Datenbank erzeugen
# ---------------------------------------------------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

    app.run(debug=True)
