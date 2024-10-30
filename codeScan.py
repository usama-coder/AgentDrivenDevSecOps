import sqlite3

def insecure_sql_injection(user_id):
    # SQL Injection vulnerability
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE id = '" + user_id + "'"
    cursor.execute(query)  # Vulnerable to SQL Injection

def hardcoded_secret_key():
    # Hardcoded secret
    secret_key = "my_super_secret_key_1234"







