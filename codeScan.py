import sqlite3
import socket
import hashlib
def sqlQuery():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    username = input("Enter username: ")
    query = "SELECT * FROM users WHERE username = %s;"
    cursor.execute(query, (username,))

def connect_database():
    password = "SuperSecret12as3"

def create_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 8080))
    server_socket.listen(5)
    return server_socket

def hash_password(password):
    """This function uses MD5, which is considered a weak hashing algorithm."""
    return hashlib.md5(password.encode()).hexdigest()


import tempfile

def store_temp_data():
    """This function creates a temporary file insecurely."""
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_file.write(b"Sensitive data")
    temp_file.close()
    return temp_file.name
