from dotenv import load_dotenv
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from .extensions import db
from .main import main as main_blueprint
from .auth import auth as auth_blueprint
from .models import User
import os


# Init app
app = Flask(__name__)

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
DB_URL = os.getenv("DATABASE_URI") or os.getenv("JAWSDB_MARIA_URL")
app.config["SQLALCHEMY_DATABASE_URI"] = DB_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.before_first_request
def setup():
    db.create_all()


# Config
app.register_blueprint(main_blueprint)
app.register_blueprint(auth_blueprint)