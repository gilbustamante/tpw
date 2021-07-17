from flask_login import UserMixin
from .extensions import db


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(40), unique=True)
    passwd = db.Column(db.String(100))
    apikey = db.Column(db.String(80))


class Currency(db.Model):
    __tablename__ = "currencies"
    currency_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300))
    icon = db.Column(db.String(300))

class Dye(db.Model):
    __tablename__ = "dyes"
    dye_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300))
    red = db.Column(db.Integer)
    blue = db.Column(db.Integer)
    green = db.Column(db.Integer)