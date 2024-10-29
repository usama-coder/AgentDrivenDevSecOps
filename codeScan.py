import subprocess

def list_directory(directory):

    command = f"ls {directory}"
    subprocess.run(command, shell=True)

def insufficient_permissions():
    # File operation without sufficient permissions
    with open("/etc/passwd", "w") as file:  # Potentially dangerous file write operation
        file.write("New user")
