import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()


def sqlQuery():
    username = input("Enter username: ")
    query = "SELECT * FROM users WHERE username = %s"
    cursor.execute(query, (username,))



def append_to_list(value, list_var=[]):
    list_var.append(value)
    return list_var

def connect_database():
    password = "SuperSecret123"  # Not secure
    # Code to connect to the database


import socket

def create_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 8080))
    server_socket.listen(5)
    return server_socket
