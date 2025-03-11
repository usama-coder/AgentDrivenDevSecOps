import streamlit as st
import pandas as pd


def render_file_viewer(vulnerabilities):
    """Displays vulnerabilities grouped by file with clickable file names."""

    st.title("📂 Vulnerabilities by File")

    # Ensure vulnerabilities exist
    if not vulnerabilities:
        st.warning("⚠️ No vulnerabilities detected!")
        return

    # Count vulnerabilities per file
    file_counts = {}
    for vuln in vulnerabilities:
        file_counts[vuln["file"]] = file_counts.get(vuln["file"], 0) + 1

    # Convert to DataFrame for display
    df = pd.DataFrame(list(file_counts.items()), columns=["File Name", "Vulnerability Count"])

    # Display as a clickable list
    st.write("### Click on a file to view vulnerabilities:")

    for index, row in df.iterrows():
        file_name = row["File Name"]
        vuln_count = row["Vulnerability Count"]

        # Create a clickable button for each file
        if st.button(f"📄 {file_name} ({vuln_count} issues)"):
            st.session_state["selected_file"] = file_name

    # Show vulnerabilities for the selected file
    if "selected_file" in st.session_state:
        selected_file = st.session_state["selected_file"]
        st.subheader(f"🔍 Issues in {selected_file}")

        for vuln in vulnerabilities:
            if vuln["file"] == selected_file:
                with st.expander(f"🛑 {vuln['description']} (Severity: {vuln['severity']})"):
                    st.code(vuln["vulnerable_code"], language="python")
