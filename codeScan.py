import sqlite3
import requests
from sqlalchemy.testing.pickleable import User


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
def log_message(user_message):
    print(user_message)

def get_user(username):
    return User.objects.filter(username=f"{username}").first()  # 🚨 Vulnerable to SQL injection

import re
pattern = re.compile("(a+)+")  # 🚨 Can cause Regex Denial of Service (ReDoS)
pattern.match("aaaaaaaaaaaaaaaaaaaa!")

