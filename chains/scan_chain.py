import subprocess
import os
import json



def scan_chain(modified_files):
    issues = []
    for file_path in modified_files:
        try:
            # Run Bandit
            result = subprocess.run(['bandit', '-f', 'json', file_path], capture_output=True, text=True)


            # Parse JSON output
            try:
                output_data = json.loads(result.stdout)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON from Bandit output on {file_path}: {e}")
                continue

            # Process each issue from Bandit's output
            if output_data.get("results"):
                for issue in output_data["results"]:
                    # Collect issue details
                    line = issue.get("line_number", 1)
                    description = issue.get("issue_text", "Unknown issue")
                    severity = issue.get("issue_severity", "LOW")
                    code =issue.get("code")

                    # Determine annotation type
                    annotation_type = "error" if severity in ["HIGH", "MEDIUM"] else "warning"
                    # Output GitHub annotation format
                    print(f"::{annotation_type} file={file_path},line={line}::{description}")

                    # Append to issues list with additional keys
                    issues.append({
                        "file": file_path,
                        "line": line,
                        "description": description,
                        "severity": severity,
                        "code" : code,

                    })

        except Exception as e:
            print(f"Error running Bandit scan on {file_path}: {e}")

    return issues




