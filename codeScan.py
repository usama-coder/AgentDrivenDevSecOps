import sqlite3
import requests

def get_data(url):

    response = requests.get(url, verify=False)
    return response.text

def insecure_sql_injection(user_id):

    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE id = '" + user_id + "'"
    cursor.execute(query)  # Vulnerable to SQL Injection

def hardcoded_secret_key():

    secret_key = "my_super_secret_key_1234"



with open("config.txt", "w") as file:
    file.write("configuration data")


class MyClass:
    def method_a(self):
        print("Method A")

    def method_b(self):
        print("Method B")

def call_method(obj, method_name):

    method = getattr(obj, method_name)
    method()



import random

def generate_token():

    return str(random.random())[2:]
