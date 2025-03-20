from ui.summary import display_summary
from ui.file_viewer import render_file_viewer
from ui.report_loader import load_vulnerabilities,fetch_reports_for_all_prs,download_report
import streamlit as st
from ui.github_status import render_github_action_status
from ui.custom_css  import apply_css

apply_css("summary.css")
st.sidebar.title("🔍 Select a Pull Request")
render_github_action_status()
# Fetch PRs and reports
pr_reports = fetch_reports_for_all_prs()
if not pr_reports:
    st.sidebar.info("🚨 No open pull requests found!")
    st.warning("No data available because no pull requests exist.")
    st.stop()

if "selected_pr" not in st.session_state:
    st.session_state["selected_pr"] = None

# Prepare PR dropdown options with dynamic target branch
if pr_reports:
    pr_options = {
        f"{data['branch']} ⟶ {data['target_branch']}": pr_number
        for pr_number, data in pr_reports.items()
    }

    if st.session_state["selected_pr"] is None:
        latest_pr_number = max(pr_options.values())
        st.session_state["selected_pr"] = latest_pr_number
        st.session_state["selected_pr_branch"] = pr_reports[latest_pr_number]["branch"]

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


