import streamlit as st

def display_summary(vulnerabilities):
    """Display a summary of security vulnerabilities with CodePen styling."""

    total_vulnerabilities = len(vulnerabilities)
    severity_counts = {"LOW": 0, "MEDIUM": 0, "HIGH": 0}

    for vuln in vulnerabilities:
        severity_counts[vuln["severity"].upper()] += 1

    st.markdown('<h2 class="summary-title">🔒 Security Scan Summary</h2>', unsafe_allow_html=True)

    # ✅ Fix Logo & Text Alignment using Flexbox
    st.markdown("""           
                <h3 class="overview-title">Overview of Detected Security Issues</h3>
          
        """, unsafe_allow_html=True)

    # ✅ Improved Metrics for Better Visibility
    col1, col2, col3, col4 = st.columns(4)
    col1.metric(label="🛡️ **Total Issues**", value=total_vulnerabilities)
    col2.metric(label="🔴 **High Severity**", value=severity_counts["HIGH"])
    col3.metric(label="🟠 **Medium Severity**", value=severity_counts["MEDIUM"])
    col4.metric(label="🟢 **Low Severity**", value=severity_counts["LOW"])

    st.write("---")

    # ✅ Styled "Vulnerabilities by File" Table
    st.subheader("📂 Vulnerabilities by File")

    if not vulnerabilities:
        st.success("✅ No vulnerabilities found!")
        return

    file_vuln_counts = {}
    for vuln in vulnerabilities:
        file_vuln_counts[vuln["file"]] = file_vuln_counts.get(vuln["file"], 0) + 1

    # ✅ Convert Data to a Table Format
    formatted_files = [{"File Name": file, "Total Issues": count} for file, count in file_vuln_counts.items()]

    # ✅ Apply Styled Table
    st.markdown('<div class="styled-table">', unsafe_allow_html=True)
    st.dataframe(formatted_files, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
