import hashlib
import subprocess
import json

def run_bandit_scan(file_path):

    issues = []
    try:
        result = subprocess.run(['bandit', '-f', 'json', file_path], capture_output=True, text=True)
        output_data = json.loads(result.stdout)

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
    issues = []
    try:
        result = subprocess.run(['safety', 'check', '--json'], capture_output=True, text=True)
        output_data = json.loads(result.stdout)

        if isinstance(output_data, list):
            for vuln in output_data:
                if isinstance(vuln, list) and len(vuln) > 1:
                    package_name = vuln[0]
                    advisory = vuln[3] if len(vuln) > 3 else "No advisory available"
                    severity = "HIGH" if len(vuln) > 2 and vuln[2] else "LOW"
                    issues.append({
                        "tool": "Safety",
                        "file": "requirements.txt",
                        "line": 1,
                        "description": f"{package_name} - {advisory}",
                        "severity": severity,
                        "code": "",
                    })
        else:
            print("Unexpected Safety JSON structure:", output_data)

    except subprocess.CalledProcessError as e:
        print(f"Error running Safety scan: {e}")
    except json.JSONDecodeError as e:
        print(f"Error decoding Safety JSON: {e}")

    return issues


# def run_semgrep_scan(files):
#
#     issues = []
#     for file_path in files:
#         try:
#             print(f"Running Semgrep on: {file_path}...")
#
#             # Run Semgrep with OWASP Top 10 rules
#             result = subprocess.run(
#                 ['semgrep', '--config', 'p/owasp-top-ten', '--json', file_path],
#                 capture_output=True,
#                 text=True
#             )
#
#             # Print raw Semgrep output
#             print(f"Raw Semgrep Output for {file_path}:\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}")
#
#             # Handle cases where Semgrep outputs nothing
#             if not result.stdout.strip():
#                 print(f"No output from Semgrep for {file_path}.")
#                 continue
#
#             # Parse JSON output from Semgrep
#             output_data = json.loads(result.stdout)
#             print(f"Parsed Semgrep Output for {file_path}: {output_data}")
#
#             # Process issues
#             if "results" in output_data:
#                 for issue in output_data["results"]:
#                     issue_details = {
#                         "file": file_path,
#                         "line": issue["start"]["line"],
#                         "description": issue["extra"]["message"],
#                         "severity": issue["extra"].get("severity", "LOW"),
#                         "vulnerable_code": issue["extra"].get("lines", "No code snippet provided"),
#                     }
#                     issues.append(issue_details)
#
#                     # Print each detected issue
#                     print(f"Issue Detected:\nFile: {file_path}\nLine: {issue_details['line']}\n"
#                           f"Description: {issue_details['description']}\nSeverity: {issue_details['severity']}\n"
#                           f"Code:\n{issue_details['vulnerable_code']}\n")
#
#         except subprocess.CalledProcessError as e:
#             print(f"Error running Semgrep on {file_path}: {e}")
#         except json.JSONDecodeError as e:
#             print(f"Error decoding JSON output for {file_path}: {e}")
#
#     print(f"Semgrep scan completed. Total issues detected: {len(issues)}")
#     return issues

def scan_chain(modified_files):

    all_issues_bandit = []
    all_issues_secrets = []

    for file_path in modified_files:
         bandit_issues = run_bandit_scan(file_path)
         all_issues_bandit.extend(bandit_issues)
         secrets = run_detect_secrets_scan(file_path)
         all_issues_secrets.extend(secrets)
    all_issues=filter_common_issues(all_issues_bandit,all_issues_secrets)

    # Run Safety (only once, since it scans dependencies in requirements.txt)
    safety_issues = run_safety_scan()
    all_issues.extend(safety_issues)
    return all_issues

def run_detect_secrets_scan(file_path):

    try:
        result = subprocess.run(["detect-secrets", "scan", file_path], capture_output=True, text=True)
        output_data = json.loads(result.stdout)

        issues = []
        for file, secrets in output_data.get("results", {}).items():
            for secret in secrets:
                issues.append({
                    "tool": "detect-secrets",
                    "file": file,
                    "line": secret.get("line_number", "Unknown"),
                    "description": f"Possible secret detected ({secret.get('type', 'Unknown')})",
                    "severity": "HIGH",
                    "code": secret.get("hashed_secret", "Hidden"),
                })
        return issues

    except Exception as e:
        print(f"Error running detect-secrets: {e}")
        return []


def generate_issue_hash(issue):

    unique_string = f"{issue['file']}:{issue['line']}"
    return hashlib.sha256(unique_string.encode()).hexdigest()


def filter_common_issues(bandit_issues, detect_secrets_issues):

    bandit_hashes = {generate_issue_hash(issue) for issue in bandit_issues}
    filtered_issues = [
        issue for issue in detect_secrets_issues if generate_issue_hash(issue) not in bandit_hashes
    ]
    # Merge Bandit's unique issues and filtered detect-secrets issues
    final_issues = bandit_issues + filtered_issues
    print(f" Filtered out {len(detect_secrets_issues) - len(filtered_issues)} common issues.")
    return final_issues

if __name__ == "__main__":
    modified_files = ["codeScan.py"]

    issues = scan_chain(modified_files)

    for issue in issues:
        print(f"Tool: {issue['tool']}, File: {issue['file']}, Line: {issue['line']}, Severity: {issue['severity']}")
        print(f"Description: {issue['description']}")
        print(f"Code: {issue['code']}")
        print("-----")
