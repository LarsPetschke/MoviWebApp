import os
from flask import Flask, request, redirect, url_for, render_template
from data_manager import DataManager
from models import db, Movie

app = Flask(__name__)

# Absoluter Pfad zur Datenbank im instance-Ordner (funktioniert lokal und auf Codio).
# Flask-SQLAlchemy 3 loest relative Pfade sonst relativ zum instance-Ordner auf
# ("instance/instance/movies.db") und kann die Datei dann nicht oeffnen.
os.makedirs(app.instance_path, exist_ok=True)
db_path = os.path.join(app.instance_path, "movies.db")
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + db_path.replace("\\", "/")

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
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
    user = data_manager.get_user(user_id)
    if user is None:
        return render_template('404.html'), 404
    movies = data_manager.get_movies(user_id)
    return render_template('movies.html', movies=movies, user_id=user_id, user=user)


# ---------------------------------------------------------
# Film hinzufügen (POST)
# ---------------------------------------------------------
@app.route('/users/<int:user_id>/movies', methods=['POST'])
def add_movie(user_id):
    title = (request.form.get('title') or '').strip()
    year = request.form.get('year', type=int)
    director = (request.form.get('director') or '').strip()
    poster_url = ""

    if not title or year is None:
        return redirect(url_for('get_movies', user_id=user_id))

    if not director:
        # Film (Titel + Jahr) in der Datenbank suchen
        known = data_manager.find_movie(title, year)
        if known:
            director = known.director
            poster_url = known.poster_url or ""
        else:
            # Nicht gefunden -> Regisseur abfragen
            return render_template('director.html', user_id=user_id,
                                   title=title, year=year)

    movie = Movie(
        name=title,
        director=director,
        year=year,
        poster_url=poster_url,
        user_id=user_id
    )

    data_manager.add_movie(movie)
    return redirect(url_for('get_movies', user_id=user_id))


# ---------------------------------------------------------
# Film aktualisieren (POST)
# ---------------------------------------------------------
@app.route('/users/<int:user_id>/movies/<int:movie_id>/update', methods=['POST'])
def update_movie(user_id, movie_id):
    new_title = request.form.get('new_title') or None
    new_year = request.form.get('new_year', type=int)
    data_manager.update_movie(movie_id, new_title, new_year)
    return redirect(url_for('get_movies', user_id=user_id))


# ---------------------------------------------------------
# Film löschen (POST)
# ---------------------------------------------------------
@app.route('/users/<int:user_id>/movies/<int:movie_id>/delete', methods=['POST'])
def delete_movie(user_id, movie_id):
    data_manager.delete_movie(movie_id)
    return redirect(url_for('get_movies', user_id=user_id))


# ---------------------------------------------------------
# 404 Fehlerseite
# ---------------------------------------------------------
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


# ---------------------------------------------------------
# App starten + Datenbank erzeugen
# ---------------------------------------------------------
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
