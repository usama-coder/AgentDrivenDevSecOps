import sqlite3
import socket
import hashlib
def sqlQuery():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    username = input("Enter username: ")
    query = "SELECT * FROM users WHERE username = %s"
cursor.execute(query, (username,))


def connect_database():
    password = input("Enter DB password: ")
    print("Connecting...")

def create_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 8080))
    server_socket.listen(5)
    return server_socket

def hash_password(password):
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

import subprocess
import yaml
import tempfile

def insecure_subprocess():
    cmd = input("Enter command: ")
    subprocess.run(cmd, shell=True)  # B602

def assert_used_as_control():
    config_loaded = False
    assert config_loaded, "Config must be loaded before proceeding."  # B101

def yaml_loader_issue():
    raw_yaml = input("Paste YAML config: ")
    config = yaml.load(raw_yaml, Loader=yaml.Loader)  # B506

def bad_tempfile():
    temp_path = tempfile.mktemp()  # B108
    with open(temp_path, "w") as f:
        f.write("insecure temp file content")
