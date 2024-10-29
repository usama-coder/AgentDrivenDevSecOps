import subprocess
import os
import json


def scan_chain(modified_files):
    issues = []
    for file_path in modified_files:
        try:
            result = subprocess.run(['bandit', '-f', 'json', file_path], capture_output=True, text=True)
            output_data = json.loads(result.stdout)

            for issue in output_data.get("results", []):
                # Example structured data for each issue
                issues.append({
                    "file": file_path,
                    "line": issue.get("line_number", 1),
                    "description": issue.get("issue_text", "Unknown issue"),
                    "severity": issue.get("issue_severity", "LOW"),
                    "bad_practice": "try:\n    some_important_code()\nexcept:\n    print('Error')",
                    "good_practice": "try:\n    some_important_code()\nexcept Exception:\n    print('Error')"
                })

        except Exception as e:
            print(f"Error running Bandit scan on {file_path}: {e}")

    return issues
def parse_bandit_output(output_data):

    issues = []
    for issue in output_data.get("results", []):
        issue_text = issue.get("issue_text", "")
        code_snippet = issue.get("code", "")  # Assuming Bandit provides code snippets

        issues.append({
            "issue_text": issue_text,
            "code": code_snippet
        })

    return issues