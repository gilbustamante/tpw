"""Populates database with GW2's dye data"""

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

def add_dyes(dye):
    """Add each dye to database"""
    try:
        statement = """
        INSERT INTO dyes (dye_id, name, red, blue, green) 
        VALUES (%s, %s, %s, %s, %s)
        """
        data = (dye["id"],
                dye["name"],
                dye["metal"]["rgb"][0],
                dye["metal"]["rgb"][1],
                dye["metal"]["rgb"][2])
        cursor.execute(statement, data)
        connection.commit()
        print(f"Added dye {dye['name']} to db.")
    except database.Error as err:
        print(f"Database Error: {err}")



try:
    for i in range(0, 4):
        url = f"https://api.guildwars2.com/v2/colors?page={i}&page_size=200"
        res = requests.get(url).json()
        for item in res:
            add_dyes(item)
except TypeError as err:
    print(f"Error: {err} (reached end of dye list?)")
