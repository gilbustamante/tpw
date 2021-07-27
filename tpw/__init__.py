from dotenv import load_dotenv
from flask import Flask, render_template
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from .extensions import db
from .main import main as main_blueprint
from .auth import auth as auth_blueprint
from .market import market as market_blueprint
from .models import User
from datetime import datetime, timezone
import timeago
import os


# Init app
app = Flask(__name__)

# 404 Error handler
@app.errorhandler(404)
def page_not_found(err):
    return render_template("errors/404.html"), 404

# 500 Error handler
@app.errorhandler(500)
def page_not_found(err):
    return render_template("errors/500.html"), 500

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
DB_URL = os.getenv("DATABASE_URI") or os.getenv("JAWSDB_MARIA_URL")
app.config["SQLALCHEMY_DATABASE_URI"] = DB_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = "auth.login_get"
login_manager.init_app(app)


# User loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Setup DB
@app.before_first_request
def setup():
    db.create_all()


# For formatting dates in templates correctly
@app.template_filter('timeago')
def fromnow(date):
    date = datetime.fromisoformat(date)
    now = datetime.now(timezone.utc)
    return timeago.format(date, now)


# Config
app.register_blueprint(main_blueprint)
app.register_blueprint(auth_blueprint)
app.register_blueprint(market_blueprint)