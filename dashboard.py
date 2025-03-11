import streamlit as st
from ui.sidebar import render_sidebar
from ui.summary import display_summary
from ui.file_viewer import render_file_viewer
from ui.report_loader import load_vulnerabilities

# Load vulnerability data from report
vulnerabilities = load_vulnerabilities()

# Streamlit App Configuration
st.set_page_config(page_title="Vulnerability Dashboard", layout="wide")

# Sidebar for Navigation
selected_page = render_sidebar()

# Show appropriate page based on selection
if selected_page == "Summary":
    display_summary()
elif selected_page == "Vulnerabilities by File":
    render_file_viewer(vulnerabilities)
