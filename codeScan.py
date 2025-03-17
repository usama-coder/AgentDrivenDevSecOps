import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

username = input("Enter username: ")
query = "SELECT * FROM users WHERE username = '" + username + "';"  # ❌ Vulnerable: SQL Injection
cursor.execute(query)



