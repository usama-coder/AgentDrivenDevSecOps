import subprocess

def list_directory(directory):

    command = f"ls {directory}"
    subprocess.run(command, shell=True)


