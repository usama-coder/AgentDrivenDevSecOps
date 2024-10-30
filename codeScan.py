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

def insufficient_permissions():
    # File operation without sufficient permissions
    with open("/etc/passwd", "w") as file:  # Potentially dangerous file write operation
        file.write("New user")

import subprocess

def delete_file(filename):
    # Vulnerable Code
    subprocess.call("rm -rf " + filename, shell=True)

import requests

import hashlib

def hash_password(password):
    # Vulnerable Code
    return hashlib.md5(password.encode()).hexdigest()

def calculate(expression):
    # Vulnerable Code
    return eval(expression)

import os

def read_file(filepath):
    # Vulnerable Code
    with open("/var/data/" + filepath, "r") as f:
        return f.read()
