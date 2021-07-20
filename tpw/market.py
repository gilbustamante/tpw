from flask import Blueprint, render_template
from flask_login import login_required, current_user
from dotenv import load_dotenv
from .models import Currency, Dye, Item
from tpw.helpers import (auth_api_call, public_api_call, format_number, format_gold,
                         find_item, check_if_undercut)

# Load environment variables
load_dotenv()

market = Blueprint("market", __name__)

@market.route("/current")
def current_listings():
    # All the URLs we'll need for this request
    sell_url = "https://api.guildwars2.com/v2/commerce/transactions/current/sells"
    buy_url = "https://api.guildwars2.com/v2/commerce/transactions/current/buys"
    delivery_url = "https://api.guildwars2.com/v2/commerce/delivery"
    price_url = "https://api.guildwars2.com/v2/commerce/prices?ids="

    # Request account's sell orders
    sells = auth_api_call(current_user.id, sell_url)

    # TODO: Request account's buy orders

    # Get item prices
    sell_id_list = [str(item["item_id"]) for item in sells]
    # TODO: buy_id_list here
    prices = public_api_call(price_url + ','.join(sell_id_list))

    # Find item and add some values for passing to template
    for order in sells:
        item = find_item(order["item_id"])
        order["name"] = item.name
        order["icon"] = item.icon
        if check_if_undercut(order, prices):
            order["undercut"] = True

    return render_template("market/current.html", sells=sells)