"""
Populates the database with GW2's currency data.
"""

import os
import requests
import mysql.connector as database
from dotenv import load_dotenv
from ..helpers import public_api_call

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

def add_currencies(currency):
    try:
        statement = """
        INSERT INTO currencies (currency_id, name, icon) VALUES (%s, %s, %s)
        """
        data = (currency["id"], currency["name"], currency["icon"])
        cursor.execute(statement, data)
        connection.commit()
        print(f"Added currency {currency['name']} to db.")
    except database.Error as e:
        print(f"Database Error: {e}")

url = "https://api.guildwars2.com/v2/currencies?ids=all"
res = public_api_call(url)

for result in res:
    add_currencies(result)