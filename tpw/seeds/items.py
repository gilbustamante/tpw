"""
ArenaNet allows 600 API requests per minute (x-rate-limit-limit).
As of this writing 'x-page-total' lists 303 pages (60446 total items) so
we should be OK iterating 303 times to grab all the items in the game.
"""

import os

import requests
import mysql.connector as database
from dotenv import load_dotenv

load_dotenv()

username = os.getenv("DB_USER")
password = os.getenv("DB_PASS")

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
    for i in range(0, 303):
        url = f"https://api.guildwars2.com/v2/items?page={i}&page_size=200"
        res = requests.get(url).json()
        for item in res:
            add_items(item)
except TypeError as e:
    print(f"Error: {e} (reached end of list?)")
