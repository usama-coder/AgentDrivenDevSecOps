import streamlit as st
from ui.report_loader import load_vulnerabilities

def display_summary():
    """Displays the vulnerability summary with counts and file-wise breakdown."""

    # Load vulnerabilities
    vulnerabilities = load_vulnerabilities()

    # Compute total vulnerabilities
    total_vulnerabilities = len(vulnerabilities)
    severity_counts = {"LOW": 0, "MEDIUM": 0, "HIGH": 0}

    for vuln in vulnerabilities:
        severity_counts[vuln["severity"].upper()] += 1

    # 🎯 Display Summary Metrics
    st.title("🔍 Security Summary")
    st.write("### Overview of Detected Security Issues")

    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
    col1.metric(label="🔴 Total Issues", value=total_vulnerabilities)
    col2.metric(label="🟡 High Severity", value=severity_counts["HIGH"])
    col3.metric(label="🟠 Medium Severity", value=severity_counts["MEDIUM"])
    col4.metric(label="🟢 Low Severity", value=severity_counts["LOW"])

    st.write("---")

    # 📂 **Display vulnerabilities per file**
    st.subheader("📂 Vulnerabilities by File")

    if not vulnerabilities:
        st.success("✅ No vulnerabilities found!")
        return

    # Group vulnerabilities by file
    file_vuln_counts = {}
    for vuln in vulnerabilities:
        file_vuln_counts[vuln["file"]] = file_vuln_counts.get(vuln["file"], 0) + 1

    # Create a formatted table for file-wise vulnerabilities
    formatted_files = [{"File Name": file, "Total Issues": count} for file, count in file_vuln_counts.items()]

    # **Ensure the table is full width**
    st.dataframe(formatted_files, use_container_width=True)


