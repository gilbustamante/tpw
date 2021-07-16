from flask import Blueprint, render_template
from flask_login import login_required, current_user
from dotenv import load_dotenv
from .helpers import auth_api_call
import requests

# Load environment variables
load_dotenv()

main = Blueprint("main", __name__)


@main.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@main.route("/wallet", methods=["GET"])
@login_required
def api_get():
    url = "https://api.guildwars2.com/v2/account/wallet"
    wallet = auth_api_call(current_user.id, url)
    return render_template("character/wallet.html", wallet=wallet)