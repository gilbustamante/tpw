"""
ArenaNet allows 600 API requests per minute (x-rate-limit-limit).  The maximum
number of items you can view per request is 200. So the number of requests we
need to make is (x-result-total/200).
"""

import os

import requests
import mysql.connector as database
import math
from time import sleep
from dotenv import load_dotenv

load_dotenv()

username = os.getenv("DB_USER")
password = os.getenv("DB_PASS")

"""
So every time ArenaNet updates the game and adds items, if any of those items
need to be displayed on the page, the app throws a fit (can't display an item
that doesn't exist yet). This means we need to "rebuild" the db every update.

I got tired of doing the math myself so I wrote the following lines to just
automatically calculate it; all you need to do is plug in whatever the current
x-result-total is in the API response headers:
"""

# TODO: Make one request, get the current x-result-total and plug it in below

total_items = 64129 # Change this to whatever the current x-result-total is
rate_limit = 200
total_pages = math.ceil(total_items/rate_limit)

connection = database.connect(
    user=username,
    password=password,
    host='localhost',
    database="tpw"
)

cursor = connection.cursor()

def add_items(item):
    """Seed database with fake user"""
    try:
        statement = "INSERT INTO items (item_id, name, icon, item_level, rarity) VALUES (%s, %s, %s, %s, %s)"
        data = (item["id"], item["name"], item["icon"], item["level"], item["rarity"])
        cursor.execute(statement, data)
        connection.commit()
        print(f"Added item {item['name']} to db.")
    except (database.Error, KeyError) as e:
        print(f"Database Error: {e}")

try:
    for i in range(0, total_pages):
        url = f"https://api.guildwars2.com/v2/items?page={i}&page_size=200"
        res = requests.get(url).json()
        for item in res:
            add_items(item)
        sleep(1) # So as not to make too many requests at once
except TypeError as e:
    print(f"Error: {e} (reached end of list?)")
