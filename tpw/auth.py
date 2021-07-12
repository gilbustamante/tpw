"""Auth routes/blueprint"""

from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from .extensions import db
from .models import User

auth = Blueprint("auth", __name__)


@auth.route("/register", methods=["GET"])
def register_get():
    return render_template("auth/register.html")


@auth.route("/register", methods=["POST"])
def register_post():
    email = request.form.get("email")
    username = request.form.get("username")
    password = request.form.get("password")
    api_key = request.form.get("apikey")

    # Redirect user if username/password already exists
    user_email = User.query.filter_by(email=email).first()
    user_name = User.query.filter_by(username=username).first()
    if user_email:
        flash("Email already registered.")
        return redirect(url_for("auth.register_get"))
    if user_name:
        flash("Username already registered.")
        return redirect(url_for("auth.register_get"))

    # Hash password and create new user
    hashed_pw = generate_password_hash(password, method="sha256")
    new_user = User(email=email,
                    username=username,
                    passwd=hashed_pw,
                    apikey=api_key)

    # Add user to DB
    db.session.add(new_user)
    db.session.commit()

    login_user(new_user)

    return redirect(url_for("main.index"))


@auth.route("/login", methods=["GET"])
def login_get():
    return render_template("auth/login.html")


@auth.route("/login", methods=["POST"])
def login_post():
    pass
