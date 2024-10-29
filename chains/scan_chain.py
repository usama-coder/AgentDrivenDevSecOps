import subprocess
import os
import json


def scan_chain(modified_files):

    issues = []
    for file_path in modified_files:
        try:
            # Run Bandit on each modified file
            result = subprocess.run(['bandit', '-f', 'json', file_path], capture_output=True, text=True)

            # Parse JSON output from Bandit
            output_data = json.loads(result.stdout)
            if output_data.get("results"):
                issues.extend(output_data["results"])  # Collect issues found in each file

        except Exception as e:
            print(f"Error running Bandit scan on {file_path}: {e}")

    return {"issues": issues}

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