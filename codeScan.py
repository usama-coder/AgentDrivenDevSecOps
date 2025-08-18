import sqlite3
import socket
import hashlib
def sqlQuery():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    username = input("Enter username: ")
    query = "SELECT * FROM users WHERE username=%s AND password=%s"
cursor.execute(query, (username, password)) OR '1'='1';"
    cursor.execute(query)


def connect_database():
    password = request.form.get('password')

def create_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 8080))
    server_socket.listen(5)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    return server_socket

def hash_password(password):
    import hashlib

def hash_password(password):
    """This function uses MD5, which is considered a weak hashing algorithm."""
    return hashlib.md5(password.encode()).hexdigest()

import random

def generate_otp():
    """This function generates an OTP using an insecure random number generator."""
    random.seed(1234)
    return random.randint(100000, 999999)

import tempfile

def store_temp_data():
    """This function creates a temporary file insecurely."""
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_file.write(b"Sensitive data")
    temp_file.close()
    import os
    os.chmod(temp_file.name, 0o777)
    return temp_file.name
