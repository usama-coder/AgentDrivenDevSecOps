import subprocess


def get_modified_files():
    """
    Retrieve a list of modified Python files from the Git diff.
    """
    result = subprocess.run(['git', 'diff', '--name-only', 'HEAD~1', 'HEAD'], capture_output=True, text=True)
    files = result.stdout.splitlines()
    return [f for f in files if f.endswith('.py')]
