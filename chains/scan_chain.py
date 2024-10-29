import subprocess
import os
import json


def scan_chain():
    try:
        # Run Bandit scan on the project directory
        code_scan_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'codeScan.py'))

        # Run Bandit with JSON output for easier parsing
        result = subprocess.run(['bandit', '-r', code_scan_path, '-f', 'json'], capture_output=True, text=True)

        # Check if output is empty (meaning no issues found)

        # Parse the JSON output if issues are found
        output_data = json.loads(result.stdout)
        if output_data.get("results"):
            print("Vulnerabilities found.")
            return {"issues": parse_bandit_output(output_data)}
        else:
            print("No vulnerabilities found.")
            return {"issues": []}
    except Exception as e:
        print(f"Error running Bandit scan: {e}")
        return {"issues": []}


def parse_bandit_output(output_data):
    """
    Processes Bandit output to extract vulnerabilities.
    """
    issues = []
    for issue in output_data.get("results", []):
        issue_text = issue.get("issue_text", "")
        code_snippet = issue.get("code", "")  # Assuming Bandit provides code snippets

        issues.append({
            "issue_text": issue_text,
            "code": code_snippet
        })

    return issues