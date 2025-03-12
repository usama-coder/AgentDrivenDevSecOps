
from sqlalchemy.testing.pickleable import User

import os

user_input = input("Enter a filename: ")
os.system("rm -rf " + user_input)  # ❌ Vulnerable: Command injection


import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

username = input("Enter username: ")
query = "SELECT * FROM users WHERE username = '" + username + "';"  # ❌ Vulnerable: SQL Injection
cursor.execute(query)
