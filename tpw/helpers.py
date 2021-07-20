from .models import User, Item
import requests

def find_user(user_id: int):
    """Retrieves user from database, given a user ID"""
    return User.query.filter_by(id=user_id).first()

def public_api_call(url: str):
    """Returns JSON from public endpoints"""
    return requests.get(url).json()

def auth_api_call(user_id: int, url: str):
    """Returns JSON from authenticated endpoints"""
    api_key = User.query.filter_by(id=user_id).first().apikey
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    return requests.get(url, headers=headers).json()

def format_number(number: int):
    """Formats large numbers with commas for readability"""
    return "{:,}".format(number)

def format_gold(number: int):
    """Formats numbers into gold, silver, and copper values"""
    number = str(number)
    if len(number) > 4:
        copper = number[-2:]
        silver = number[-4:-2]
        gold = number[:-4]
        return f"""{gold} <img src="/static/images/gold.png">
                   {silver} <img src="/static/images/silver.png"> 
                   {copper} <img src="/static/images/copper.png">"""
    elif len(number) > 2:
        copper = number[-2:]
        silver = number[:-2]
        return f"""{silver} <img src="/static/images/silver.png"> 
                   {copper} <img src="/static/images/copper.png">"""
    else:
        return f"""{copper} <img src="/static/images/copper.png">"""

def find_item(item_id: int):
    """Retrieves item information from database"""
    return Item.query.filter_by(item_id=item_id).first()

def check_if_undercut(order: dict, prices: list):
    """Determines if order has been undercut"""
    for price in prices:
        item_undercut = (
            # If item ID matches...
            price["id"] == order["item_id"]
            # ...and the lowest price is below our item's price
            and price["sells"]["unit_price"] < order["price"]
        )
        if item_undercut:
            return True