from flask import Blueprint, render_template
from flask_login import login_required, current_user
from dotenv import load_dotenv
from .helpers import create_request_header, auth_api_call
import requests

# Load environment variables
load_dotenv()

main = Blueprint("main", __name__)


@main.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@main.route("/api", methods=["GET"])
@login_required
def api_get():
    url = "https://api.guildwars2.com/v2/account"
    res = auth_api_call(current_user.id, url)
    return res