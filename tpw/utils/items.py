"""
ArenaNet allows 600 API requests per minute (x-rate-limit-limit).
As of this writing 'x-page-total' lists 303 pages (60444 total items) so
we should be OK iterating 303 times to grab all the items in the game.
"""

import requests
import os
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

# TODO: Update this for market items

def add_data(email, username, password, apikey):
    """Seed database with fake user"""
    try:
        statement = "INSERT INTO users (email, username, passwd, apikey) VALUES (%s, %s, %s, %s)"
        data = (email, username, password, apikey)
        cursor.execute(statement, data)
        connection.commit()
        print(f"Added user {username} to database.")
    except database.Error as e:
        print(f"Database Error: {e}")


if __name__ == '__main__':
    add_data('hoophappy@hotmeal.comma', 'Hooper', '12345', '0000000000000000')
    add_data('snaptastic@gorf.worf', 'Snapper', '12345', '0000000000000000')