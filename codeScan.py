import sqlite3
import socket
import hashlib
def sqlQuery():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    username = input("Enter username: ")
    query = "SELECT * FROM users WHERE username = '" + username + "';"
    cursor.execute(query)

def connect_database():
    password = "SuperSecret123"

def create_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 8080))
    server_socket.listen(5)
    return server_socket



def hash_password(password):
    """This function uses MD5, which is considered a weak hashing algorithm."""
    return hashlib.sha256(password.encode()).hexdigest()

import random

def generate_otp():
    """This function generates an OTP using an insecure random number generator."""
    return random.randint(100000, 999999)

import tempfile

def store_temp_data():
    """This function creates a temporary file insecurely."""
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_file.write(b"Sensitive data")
    temp_file.close()
    return temp_file.name
