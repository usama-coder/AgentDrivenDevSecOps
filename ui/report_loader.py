import requests
import zipfile
import io
import streamlit as st
import re

def fetch_latest_report():
    GITHUB_TOKEN = st.secrets["GITHUB_TOKEN"]
    REPO_OWNER =st.secrets["REPO_OWNER"]
    REPO_NAME = st.secrets["REPO_NAME"]
    ARTIFACT_NAME =  st.secrets["ARTIFACT_NAME"]

    headers = {"Authorization": f"token {GITHUB_TOKEN}"}

    # Get artifact metadata
    artifacts_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/actions/artifacts"
    response = requests.get(artifacts_url, headers=headers)

    if response.status_code != 200:
        st.error("❌ Failed to fetch artifacts. Check token/repo settings.")
        return None

    artifacts = response.json().get("artifacts", [])
    latest_artifact = next((a for a in artifacts if a["name"] == ARTIFACT_NAME), None)

    if not latest_artifact:
        st.error("⚠️ No recent vulnerability reports found.")
        return None

    # Download the artifact
    download_url = latest_artifact["archive_download_url"]
    response = requests.get(download_url, headers=headers, stream=True)

    if response.status_code == 200:
        # Unzip the artifact and extract vulnerability_report.md
        with zipfile.ZipFile(io.BytesIO(response.content), "r") as zip_ref:
            for file in zip_ref.namelist():
                if file.endswith("vulnerability_report.md"):  # Extract the correct file
                    with zip_ref.open(file) as report_file:
                        return report_file.read().decode("utf-8")  # Return report content

    st.error("❌ Failed to extract vulnerability report from artifact.")
    return None


# def load_vulnerabilities():
#     content = fetch_latest_report()
#     content = fetch_reports_for_all_prs()
#     if not content:
#         return []
#
#     vulnerabilities = []
#     entries = content.split("----------------------------------------")
#
#     for entry in entries:
#         if not entry.strip():
#             continue
#
#         file_match = re.search(r"### File: (.*?), Line: (\d+)", entry)
#         if not file_match:
#             continue
#
#         file_name = file_match.group(1).strip()
#         line_number = file_match.group(2).strip()
#
#         description_match = re.search(r"\*\*Description\*\*: (.*?)\n", entry, re.DOTALL)
#         description = description_match.group(1).strip() if description_match else "No description provided."
#
#         severity_match = re.search(r"\*\*Severity\*\*: (.*?)\n", entry, re.DOTALL)
#         severity = severity_match.group(1).strip() if severity_match else "LOW"
#
#         vulnerable_code_match = re.search(r"#### Vulnerable Code\n```python\n(.*?)```", entry, re.DOTALL)
#         vulnerable_code = vulnerable_code_match.group(1).strip() if vulnerable_code_match else "No vulnerable code provided."
#
#         fix_match = re.search(r"#### Recommended Fix Code\n```python\n(.*?)```", entry, re.DOTALL)
#         recommended_fix = fix_match.group(1).strip() if fix_match else "No recommended fix provided."
#
#         recommendation_match = re.search(r"#### Recommendation Description\n(.*?)\n", entry, re.DOTALL)
#         recommendation_description = recommendation_match.group(1).strip() if recommendation_match else "No recommendation provided."
#
#         vulnerabilities.append({
#             "file": file_name,
#             "line": int(line_number),
#             "description": description,
#             "severity": severity,
#             "vulnerable_code": vulnerable_code,
#             "recommended_fix": recommended_fix,
#             "recommendation_description": recommendation_description
#         })
#
#     print(f"✅ Extracted {len(vulnerabilities)} vulnerabilities successfully!")
#     return vulnerabilities
def load_vulnerabilities():
    """Load and parse the vulnerability report from the selected PR or latest available report."""

    if "selected_pr" in st.session_state and st.session_state["selected_pr"]:
        pr_reports = fetch_reports_for_all_prs()
        selected_pr_number = st.session_state["selected_pr"]

        if selected_pr_number in pr_reports:
            content = download_report(pr_reports[selected_pr_number]["archive_download_url"])
        else:
            st.error("❌ Selected PR report not found.")
            return []
    else:
        # Load the latest report when no PR is selected (first run)
        content = fetch_latest_report()

    if not content:
        return []

    vulnerabilities = []
    entries = content.split("----------------------------------------")

    for entry in entries:
        if not entry.strip():
            continue

        file_match = re.search(r"### File: (.*?), Line: (\d+)", entry)
        if not file_match:
            continue

        file_name = file_match.group(1).strip()
        line_number = file_match.group(2).strip()

        description_match = re.search(r"\*\*Description\*\*: (.*?)\n", entry, re.DOTALL)
        description = description_match.group(1).strip() if description_match else "No description provided."

        severity_match = re.search(r"\*\*Severity\*\*: (.*?)\n", entry, re.DOTALL)
        severity = severity_match.group(1).strip() if severity_match else "LOW"

        vulnerable_code_match = re.search(r"#### Vulnerable Code\n```python\n(.*?)```", entry, re.DOTALL)
        vulnerable_code = vulnerable_code_match.group(1).strip() if vulnerable_code_match else "No vulnerable code provided."

        fix_match = re.search(r"#### Recommended Fix Code\n```python\n(.*?)```", entry, re.DOTALL)
        recommended_fix = fix_match.group(1).strip() if fix_match else "No recommended fix provided."

        recommendation_match = re.search(r"#### Recommendation Description\n(.*?)\n", entry, re.DOTALL)
        recommendation_description = recommendation_match.group(1).strip() if recommendation_match else "No recommendation provided."

        vulnerabilities.append({
            "file": file_name,
            "line": int(line_number),
            "description": description,
            "severity": severity,
            "vulnerable_code": vulnerable_code,
            "recommended_fix": recommended_fix,
            "recommendation_description": recommendation_description
        })

    print(f"✅ Extracted {len(vulnerabilities)} vulnerabilities successfully!")
    return vulnerabilities

def fetch_reports_for_all_prs():
    """Fetch open PRs and their corresponding reports."""
    GITHUB_TOKEN = st.secrets["GITHUB_TOKEN"]
    REPO_OWNER = st.secrets["REPO_OWNER"]
    REPO_NAME = st.secrets["REPO_NAME"]
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}

    # Step 1: Fetch Open PRs
    prs_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/pulls?state=open"
    prs_response = requests.get(prs_url, headers=headers)
    if prs_response.status_code != 200:
        st.error("❌ Failed to fetch open pull requests.")
        return {}

    prs = prs_response.json()  # Convert response to a proper Python list

    # Step 2: Fetch Artifacts
    artifacts_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/actions/artifacts"
    artifacts_response = requests.get(artifacts_url, headers=headers)
    if artifacts_response.status_code != 200:
        st.error("❌ Failed to fetch artifacts.")
        return {}

    artifacts = artifacts_response.json().get("artifacts", [])
    pr_reports = {}

    # Step 3: Map PRs to their reports
    for pr in prs:
        pr_number = pr["number"]
        artifact_name = f"Vulnerability Report-pr-{pr_number}"
        artifact = next((a for a in artifacts if a["name"] == artifact_name), None)

        if artifact:
            pr_reports[pr_number] = {
                "title": pr["title"],
                "branch": pr["head"]["ref"],  # Store branch name correctly
                "archive_download_url": artifact["archive_download_url"]
            }

    return pr_reports


def download_report(download_url):
    """Download and extract the vulnerability report from an artifact."""
    GITHUB_TOKEN = st.secrets["GITHUB_TOKEN"]
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}

    response = requests.get(download_url, headers=headers, stream=True)
    if response.status_code == 200:
        with zipfile.ZipFile(io.BytesIO(response.content), "r") as zip_ref:
            for file in zip_ref.namelist():
                if file.endswith("vulnerability_report.md"):  # Ensure correct file is extracted
                    with zip_ref.open(file) as report_file:
                        return report_file.read().decode("utf-8")

    st.error("❌ Failed to extract vulnerability report from artifact.")
    return None