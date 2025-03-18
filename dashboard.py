import streamlit as st
from ui.sidebar import render_sidebar
from ui.summary import display_summary
from ui.file_viewer import render_file_viewer
from ui.report_loader import load_vulnerabilities

# ✅ Function to Load CSS File
def load_css(file_paths):
    """Dynamically load multiple CSS files."""
    for file_path in file_paths:
        with open(file_path, "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ✅ Load vulnerability data
vulnerabilities = load_vulnerabilities()

# ✅ Set Streamlit Page Config
st.set_page_config(page_title="Vulnerability Dashboard", layout="wide", page_icon="🛡️")

# ✅ Apply CSS from multiple files
load_css([
    "ui/styles/global.css",
    "ui/styles/dashboard.css"
])

# ✅ Add a Logo
st.markdown("""
    <div class="logo-container">
        <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/Shield_check.svg/2048px-Shield_check.svg.png" width="80">
        <h1 class="dashboard-title">Vulnerability Dashboard</h1>
    </div>
""", unsafe_allow_html=True)

# ✅ Sidebar Navigation
selected_page = render_sidebar()

# ✅ Show Appropriate Page
if selected_page == "Summary":
    display_summary()
elif selected_page == "Vulnerabilities by File":
    render_file_viewer(vulnerabilities)
