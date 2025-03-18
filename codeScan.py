import sqlite3
import socket


def sqlQuery():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    username = input("Enter username: ")
    query = "SELECT * FROM users WHERE username=%s"  # ✅ Fixed: SQL Injection
cursor.execute(query, (username,))


def connect_database():
    password = "SuperSecret123"

def create_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 8080))
    server_socket.listen(5)
    return server_socket