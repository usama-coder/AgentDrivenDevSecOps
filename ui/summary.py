import streamlit as st
from ui.report_loader import load_vulnerabilities

def load_summary_css():
    with open("ui/styles/summary.css", "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def display_summary():

    load_summary_css()
    vulnerabilities = load_vulnerabilities()
    total_vulnerabilities = len(vulnerabilities)
    severity_counts = {"LOW": 0, "MEDIUM": 0, "HIGH": 0}

    for vuln in vulnerabilities:
        severity_counts[vuln["severity"].upper()] += 1

    st.markdown('<h2 class="summary-title">🔒 Security Scan Summary</h2>', unsafe_allow_html=True)


    st.markdown("""
        <div class="logo-container">
            <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/Shield_check.svg/2048px-Shield_check.svg.png" width="60">
            <h3 class="overview-title">Overview of Detected Security Issues</h3>
        </div>
    """, unsafe_allow_html=True)

    # Metric Columns
    col1, col2, col3, col4 = st.columns(4)
    col1.metric(label="🛡️ Total Issues", value=total_vulnerabilities)
    col2.metric(label="🟡 High Severity", value=severity_counts["HIGH"])
    col3.metric(label="🟠 Medium Severity", value=severity_counts["MEDIUM"])
    col4.metric(label="🟢 Low Severity", value=severity_counts["LOW"])

    st.write("---")
    st.subheader("📂 Vulnerabilities by File")

    if not vulnerabilities:
        st.success("✅ No vulnerabilities found!")
        return

    file_vuln_counts = {}
    for vuln in vulnerabilities:
        file_vuln_counts[vuln["file"]] = file_vuln_counts.get(vuln["file"], 0) + 1

    formatted_files = [{"#": i + 1, "File Name": file, "Total Issues": count}
                       for i, (file, count) in enumerate(file_vuln_counts.items())]

    st.dataframe(formatted_files, use_container_width=True)
