from flask import Blueprint, render_template
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


main = Blueprint("main", __name__)


@main.route("/", methods=["GET"])
def index():
    return render_template("index.html")