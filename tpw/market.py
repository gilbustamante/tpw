from flask import Blueprint, render_template
from flask_login import login_required, current_user
from dotenv import load_dotenv
from tpw.helpers import auth_api_call, public_api_call, format_number, format_gold
from .models import Currency, Dye

# Load environment variables
load_dotenv()

market = Blueprint("market", __name__)

@market.route("/current")
def current_listings():
    return render_template("market/current.html")