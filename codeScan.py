import subprocess

def list_directory(directory):
    # Vulnerable to command injection
    command = f"ls {directory}"
    subprocess.run(command, shell=True)
