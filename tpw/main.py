from flask import Blueprint, render_template
from flask_login import login_required, current_user
from dotenv import load_dotenv
from tpw.helpers import auth_api_call, public_api_call, format_number, format_gold
from .models import Currency
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
    for item in wallet:
        curr = Currency.query.filter_by(currency_id=item["id"]).first()
        item["name"] = curr.name
        item["icon"] = curr.icon
        if item["name"] == 'Coin':
            item["value"] = format_gold(item["value"])
        else:
            item["value"] = format_number(item["value"])
    return render_template("character/wallet.html", wallet=wallet)