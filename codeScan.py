import sqlite3
import socket
import hashlib
def sqlQuery():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    username = input("Enter username: ")
    query = "SELECT * FROM users WHERE username = '" + username + "' OR '1'='1';"  # B608: SQL injection
    cursor.execute(query)


def connect_database():
    password = "SuperSecret12as3"
    print("Connecting with password:", password)  # B105: Hardcoded password

def create_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 8080))
    server_socket.listen(5)
    return server_socket

def hash_password(password):
    import hashlib

def hash_password(password):
    """This function uses MD5, which is considered a weak hashing algorithm."""
    return hashlib.md5(password.encode()).hexdigest()  # B303: MD5 is insecure

import random

def generate_otp():
    """This function generates an OTP using an insecure random number generator."""
    random.seed(1234)  # B311: Insecure randomness
    return random.randint(100000, 999999)

import tempfile

def store_temp_data():
    """This function creates a temporary file insecurely."""
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_file.write(b"Sensitive data")
    temp_file.close()
    import os
    os.chmod(temp_file.name, 0o777)  # B103: World writable file
    return temp_file.name
