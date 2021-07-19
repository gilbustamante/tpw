from flask import Blueprint, render_template, url_for
from flask_login import login_required, current_user
from dotenv import load_dotenv
from tpw.helpers import auth_api_call, public_api_call, format_number, format_gold
from .models import Currency, Dye, Item

# Load environment variables
load_dotenv()

main = Blueprint("main", __name__)


@main.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@main.route("/wallet", methods=["GET"])
@login_required
def wallet():
    # Retrieve wallet info
    url = "https://api.guildwars2.com/v2/account/wallet"
    res = auth_api_call(current_user.id, url)

    for item in res:
        curr = Currency.query.filter_by(currency_id=item["id"]).first()
        item["name"] = curr.name
        item["icon"] = curr.icon

        # Use the format_gold helper to correctly format coin values
        if item["name"] == 'Coin':
            item["value"] = format_gold(item["value"])
        # Otherwise just format normally
        else:
            item["value"] = format_number(item["value"])
    return render_template("character/wallet.html", wallet=wallet)

@main.route("/dyes", methods=["GET"])
@login_required
def dyes():
    # Retrieve dye IDs
    url = "https://api.guildwars2.com/v2/account/dyes"
    res = auth_api_call(current_user.id, url)

    dyes = list()
    for i in res:
        dye = Dye.query.filter_by(dye_id=i).first()
        dyes.append(dye)
    return render_template("character/dyes.html", dyes=dyes)


@main.route("/bank", methods=["GET"])
@login_required
def bank():
    # Retrieve bank items
    url = "https://api.guildwars2.com/v2/account/bank"
    res = auth_api_call(current_user.id, url)
    mutable_items = list(res)

    # For keeping track of empty bank slots
    free = 0 

    for item in mutable_items:
        # If value is None, there is no item in that slot
        if item is None:
            free += 1 
            continue

        # Find item details in database
        item_obj = Item.query.filter_by(item_id=item["id"]).first()

        # GW2 item API doesn't whitelist an item until it has been interacted
        # with by a user. A few years back the main whitelist was "lost" and
        # had to be recreated by ArenaNet. This causes old items to return None
        # even though they are actually in the user's bank, requiring this second
        # check. What a pain...
        if item_obj is None:
            item["name"] = "Unknown Item"
            item["icon"] = f"{url_for('static', filename='images/unknown.png')}"
            continue

        # Assign details to item
        item["name"] = item_obj.name
        item["icon"] = item_obj.icon
        item["item_level"] = item_obj.item_level
        item["rarity"] = item_obj.rarity

    return render_template("character/bank.html", items=mutable_items, free=free)