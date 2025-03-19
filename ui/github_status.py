import requests
import streamlit as st

def fetch_github_action_status():
    """Fetch the latest GitHub Action workflow run status for the repository."""
    GITHUB_TOKEN = st.secrets["GITHUB_TOKEN"]
    REPO_OWNER = st.secrets["REPO_OWNER"]
    REPO_NAME = st.secrets["REPO_NAME"]

    headers = {"Authorization": f"token {GITHUB_TOKEN}"}

    # Fetch latest workflow runs
    workflow_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/actions/runs"
    response = requests.get(workflow_url, headers=headers)

    if response.status_code != 200:
        return "❌ Failed to fetch GitHub Action status.", None, None

    runs = response.json().get("workflow_runs", [])
    if not runs:
        return "No recent workflow runs found.", None, None

    # Get the latest run
    latest_run = runs[0]  # Most recent workflow run
    status = latest_run["status"]  # completed, in_progress, queued
    conclusion = latest_run.get("conclusion", "Running")  # success, failure, neutral, etc.
    action_url = latest_run["html_url"]  # Link to GitHub Actions run

    return status, conclusion, action_url


def render_github_action_status():
    """Render GitHub Actions Status in the Streamlit Sidebar."""
    status, conclusion, action_url = fetch_github_action_status()

    status_colors = {
        "queued": "🟡 Queued",
        "in_progress": "🔵 Running",
        "completed": "✅ Completed",
        "failure": "❌ Failed"
    }

    conclusion_colors = {
        "success": "✅ Success",
        "failure": "❌ Failed",
        "neutral": "⚪ Neutral"
    }

    st.sidebar.title("🔄 GitHub Action Status")

    if status in status_colors:
        st.sidebar.info(f"**Workflow Status:** {status_colors[status]}")
    else:
        st.sidebar.info("🔄 Checking workflow status...")

    if status == "completed" and conclusion in conclusion_colors:
        st.sidebar.success(f"**Conclusion:** {conclusion_colors[conclusion]}")
    elif status == "in_progress":
        st.sidebar.warning("🟡 GitHub Action is currently running...")

    # Provide a link to the workflow run
    if action_url:
        st.sidebar.markdown(f"[🔍 View Workflow Details]({action_url})")

    # Refresh Button to Check Status
    if st.sidebar.button("🔄 Refresh Status"):
        st.rerun()
