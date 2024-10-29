import subprocess
import os
import json


def scan_chain(modified_files):
    issues = []
    for file_path in modified_files:
        try:
            # Run Bandit or similar tool
            result = subprocess.run(['bandit', '-f', 'json', file_path], capture_output=True, text=True)
            output_data = json.loads(result.stdout)
            if output_data.get("results"):
                for issue in output_data["results"]:
                    # Collect issue details
                    line = issue.get("line_number", 1)
                    description = issue.get("issue_text", "Unknown issue")
                    severity = issue.get("issue_severity", "LOW")

                    # Determine annotation type
                    annotation_type = "error" if severity in ["HIGH", "MEDIUM"] else "warning"
                    # Output GitHub annotation format
                    print(f"::{annotation_type} file={file_path},line={line}::{description}")

                    # Append to issues list if needed for further processing
                    issues.append({
                        "file": file_path,
                        "line": line,
                        "description": description,
                        "severity": severity
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