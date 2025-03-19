import streamlit as st
from ui.sidebar import render_sidebar
from ui.summary import display_summary
from ui.file_viewer import render_file_viewer
from ui.report_loader import load_vulnerabilities,fetch_reports_for_all_prs,download_report
import streamlit as st
import json
# ✅ Function to Load CSS File
def load_css(file_paths):
    """Dynamically load multiple CSS files."""
    for file_path in file_paths:
        with open(file_path, "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
st.sidebar.title("🔍 Select a Pull Request")

# Fetch PRs and reports
pr_reports = fetch_reports_for_all_prs()

if pr_reports:
    # Fix: Ensure `pr_reports` contains dictionaries, not strings
    pr_options = {f"{data['title']} | {data['branch']}": pr_number for pr_number, data in pr_reports.items()}

    # Auto-select latest PR on first run
    if "selected_pr" not in st.session_state:
        st.session_state["selected_pr"] = max(pr_options.values())  # Latest PR number

    # Dropdown for PR selection
    selected_pr_label = st.sidebar.selectbox("Choose a PR", options=pr_options.keys())

    # Update selected PR in session state
    selected_pr_number = pr_options[selected_pr_label]
    if selected_pr_number != st.session_state["selected_pr"]:
        st.session_state["selected_pr"] = selected_pr_number

    # Load vulnerabilities for selected PR
    vulnerabilities = load_vulnerabilities()

    # Sidebar Navigation
    selected_page = st.sidebar.radio("Navigate", ["Summary", "Vulnerabilities by File"])

    # Render pages based on selection
    if selected_page == "Summary":
        if vulnerabilities:
            display_summary(vulnerabilities)
        else:
            st.info("No data available for this PR.")

    elif selected_page == "Vulnerabilities by File":
        if vulnerabilities:
            render_file_viewer(vulnerabilities)
        else:
            st.info("No data available for this PR.")