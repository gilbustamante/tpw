"""Auth routes/blueprint"""

from flask import Blueprint, render_template, redirect, url_for, request, flash, abort, request
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from is_safe_url import is_safe_url
from .extensions import db
from tpw.helpers import find_user
from .models import User

auth = Blueprint("auth", __name__)

# The JawsDB service only allows 5MB of database storage for basic accounts.
# The database for this app totals just over 8MB, meaning I am able to migrate
# it but the INSERT privilege for the account is disabled while the size
# is > 5MB. This means new users are unable to register (can't INSERT the
# user's info into the DB). As a result registration is temporarily disabled.
@auth.route("/register", methods=["GET"])
@login_required # "disables" registration
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
        flash("Email already registered.", "error")
        return redirect(url_for("auth.register_get"))
    if user_name:
        flash("Username already registered.", "error")
        return redirect(url_for("auth.register_get"))

    # Hash password and create new user
    hashed_pw = generate_password_hash(password, method="sha256")
    new_user = User(email=email, username=username,
                    passwd=hashed_pw, apikey=api_key)

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
    username = request.form.get("username")
    password = request.form.get("password")
    remember = True if request.form.get("remember") else False
    user = User.query.filter_by(username=username).first()

    # Check if non-existent user or if password is incorrect
    if not user or not check_password_hash(user.passwd, password):
        flash("Wrong username or password. Please try again.", "error")
        return redirect(url_for("auth.login_get"))

    # Log user in
    login_user(user, remember=remember)
    
    # If user was redirected to login form, send them back
    next = request.args.get("next")
    if next and not is_safe_url(next, request.host_url):
        flash("Invalid URL. Please try again.", "error")
        return redirect(url_for("auth.login_get"))
    return redirect(next or url_for("main.index"))


@auth.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))

@auth.route("/profile", methods=["GET"])
@login_required
def profile_get():
    user = find_user(current_user.id)
    return render_template("auth/profile.html", user=user)

@auth.route("/profile", methods=["POST"])
@login_required
def profile_post():
    email = request.form.get("email")
    api_key = request.form.get("apikey")

    user = find_user(current_user.id)
    user.email = email
    user.apikey = api_key
    db.session.commit()
    flash("User details updated.", "success")
    return redirect(url_for("auth.profile_get"))
