from flask import Flask
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

# Test-Route
@app.route('/')
def home():
    return "Welcome to MoviWeb App!"

# Neue Route: Liste aller Nutzer
@app.route('/users')
def list_users():
    users = data_manager.get_users()
    return str(users)  # Temporäre Ausgabe
    # Später ersetzen wir das durch ein Template

# App starten + Datenbank erzeugen
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
