import subprocess
import os
import json



def scan_chain(modified_files):
    issues = []
    for file_path in modified_files:
        try:
            # Run Bandit
            result = subprocess.run(['bandit', '-f', 'json', file_path], capture_output=True, text=True)

            # Check if Bandit ran successfully
            if result.returncode != 0:
                print(f"Error running Bandit on {file_path}: {result.stderr}")
                continue

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

                    # Determine annotation type
                    annotation_type = "error" if severity in ["HIGH", "MEDIUM"] else "warning"
                    # Output GitHub annotation format
                    print(f"::{annotation_type} file={file_path},line={line}::{description}")

                    # Define default bad and good practices based on the issue description
                    bad_practice = "Example of vulnerable code not provided."
                    good_practice = "Example of secure code not provided."

                    # Customize examples based on description keywords
                    if "subprocess" in description:
                        bad_practice = "subprocess.run(command, shell=True)"
                        good_practice = "subprocess.run(shlex.split(command))"
                    elif "exec" in description:
                        bad_practice = "exec(untrusted_input)"
                        good_practice = "Avoid using exec() with untrusted input."

                    # Append to issues list with additional keys
                    issues.append({
                        "file": file_path,
                        "line": line,
                        "description": description,
                        "severity": severity,
                        "bad_practice": bad_practice,
                        "good_practice": good_practice
                    })

        except Exception as e:
            print(f"Error running Bandit scan on {file_path}: {e}")

    return issues




