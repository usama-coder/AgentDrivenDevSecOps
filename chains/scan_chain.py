import subprocess
import os
import json


def run_bandit_scan(file_path):
    """Run Bandit scan and return the results."""
    issues = []
    try:
        result = subprocess.run(['bandit', '-f', 'json', file_path], capture_output=True, text=True)
        output_data = json.loads(result.stdout)

        # Process each issue from Bandit's output
        if output_data.get("results"):
            for issue in output_data["results"]:
                line = issue.get("line_number", 1)
                description = issue.get("issue_text", "Unknown issue")
                severity = issue.get("issue_severity", "LOW")
                code = issue.get("code")

                annotation_type = "error" if severity in ["HIGH", "MEDIUM"] else "warning"
                print(f"::{annotation_type} file={file_path},line={line}::{description}")

                issues.append({
                    "tool": "Bandit",
                    "file": file_path,
                    "line": line,
                    "description": description,
                    "severity": severity,
                    "code": code,
                })
    except subprocess.CalledProcessError as e:
        print(f"Error running Bandit on {file_path}: {e}")
    except json.JSONDecodeError as e:
        print(f"Error decoding Bandit JSON for {file_path}: {e}")

    return issues


def run_safety_scan():
    """Run Safety scan for dependencies and return the results."""
    issues = []
    try:
        # Run Safety with JSON output
        result = subprocess.run(['safety', 'check', '--json'], capture_output=True, text=True)

        # Parse the output into a Python object
        output_data = json.loads(result.stdout)

        # Safety outputs a dictionary, but "vulnerabilities" is typically a key


        # Process each vulnerability
        for vuln in output_data:
            description = f"{vuln['package_name']} - {vuln['advisory']}"
            severity = "HIGH" if vuln.get("vulnerable_spec") else "LOW"

            issues.append({
                "tool": "Safety",
                "file": "requirements.txt",
                "line": 1,
                "description": description,
                "severity": severity,
                "code": "",  # Safety is dependency-based, so no specific code snippet
            })
    except subprocess.CalledProcessError as e:
        print(f"Error running Safety scan: {e}")
    except json.JSONDecodeError as e:
        print(f"Error decoding Safety JSON: {e}")

    return issues

import subprocess
import json

import subprocess
import json

def run_semgrep_scan(files):
    """
    Run Semgrep scan on the given files and return the results.
    Uses print statements for step-by-step visibility.
    """
    issues = []
    for file_path in files:
        try:
            print(f"Running Semgrep on: {file_path}...")

            # Run Semgrep with OWASP Top 10 rules
            result = subprocess.run(
                ['semgrep', '--config', 'p/security/owasp-top-ten', '--json', file_path],
                capture_output=True,
                text=True
            )

            # Print raw Semgrep output
            print(f"Raw Semgrep Output for {file_path}:\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}")

            # Handle cases where Semgrep outputs nothing
            if not result.stdout.strip():
                print(f"No output from Semgrep for {file_path}.")
                continue

            # Parse JSON output from Semgrep
            output_data = json.loads(result.stdout)
            print(f"Parsed Semgrep Output for {file_path}: {output_data}")

            # Process issues
            if "results" in output_data:
                for issue in output_data["results"]:
                    issue_details = {
                        "file": file_path,
                        "line": issue["start"]["line"],
                        "description": issue["extra"]["message"],
                        "severity": issue["extra"].get("severity", "LOW"),
                        "vulnerable_code": issue["extra"].get("lines", "No code snippet provided"),
                    }
                    issues.append(issue_details)

                    # Print each detected issue
                    print(f"Issue Detected:\nFile: {file_path}\nLine: {issue_details['line']}\n"
                          f"Description: {issue_details['description']}\nSeverity: {issue_details['severity']}\n"
                          f"Code:\n{issue_details['vulnerable_code']}\n")

        except subprocess.CalledProcessError as e:
            print(f"Error running Semgrep on {file_path}: {e}")
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON output for {file_path}: {e}")

    print(f"Semgrep scan completed. Total issues detected: {len(issues)}")
    return issues



def scan_chain(modified_files):
    """Run all scans on the modified files."""
    all_issues = []

    # Run Bandit on each file
    for file_path in modified_files:
         bandit_issues = run_bandit_scan(file_path)
         all_issues.extend(bandit_issues)

    # Run Safety (only once, since it scans dependencies in requirements.txt)
    #safety_issues = run_safety_scan()
   # all_issues.extend(safety_issues)

    # Run Semgrep on each file
    for file_path in modified_files:
         semgrep_issues = run_semgrep_scan(file_path)
         all_issues.extend(semgrep_issues)

    return all_issues


if __name__ == "__main__":
    modified_files = ["codeScan.py"]

    issues = scan_chain(modified_files)

    for issue in issues:
        print(f"Tool: {issue['tool']}, File: {issue['file']}, Line: {issue['line']}, Severity: {issue['severity']}")
        print(f"Description: {issue['description']}")
        print(f"Code: {issue['code']}")
        print("-----")
