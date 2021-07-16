from flask import Blueprint, render_template
from flask_login import login_required
from dotenv import load_dotenv

# TODO: Add a helper function that returns the auth 'bearer' string

# Load environment variables
load_dotenv()

main = Blueprint("main", __name__)


@main.route("/", methods=["GET"])
def index():
    return render_template("index.html")
