import re
import streamlit as st
import hashlib
from chains.remediation_chain import (
    extract_function_from_file,
    llm_replace_vulnerability,
    overwrite_function_in_file
)
def clean_recommended_fix(recommended_fix):
    """Remove unwanted Markdown-style code block markers from recommended fix."""
    cleaned_fix = re.sub(r"```[a-zA-Z]*\n?", "", recommended_fix)
    cleaned_fix = cleaned_fix.strip()
    return cleaned_fix.strip()
def apply_fix(issue):
    """Extract function, replace vulnerability using LLM, and apply changes."""
    file_name = issue["file"]
    line_number = issue["line"]
    print(f"recommended fix before cleaning {issue['recommended_fix']}")
    recommended_fix = clean_recommended_fix(issue["recommended_fix"])
    print(f"recommended fix after cleaning {issue['recommended_fix']}")
    extracted_function = extract_function_from_file(file_name, line_number)
    if not is_valid_python_code(recommended_fix):
        st.warning(
            f"⚠️ The recommended fix for `{file_name}` at line `{line_number}` is not a direct code replacement.")
        st.markdown("### Suggested Manual Fix:")
        st.info(issue["recommended_fix"])  # Show the suggested fix in an informative box
        return  # Stop execution, do not proceed with automatic replacement
    if extracted_function:
        # Use LLM to replace the vulnerability
        fixed_function = llm_replace_vulnerability(
            extracted_function, issue["vulnerable_code"],recommended_fix
        )

        # Overwrite the file with the LLM-fixed function
        overwrite_function_in_file(file_name, extracted_function, fixed_function)

        st.success(f"✅ LLM Applied Fix to {file_name} at Line {line_number}!")
    else:
        st.error("⚠️ Could not find the function to fix.")


def render_file_viewer(vulnerabilities):
    """Display vulnerabilities grouped by file, ensuring no duplicate file entries."""
    if not vulnerabilities:
        st.info("✅ No vulnerabilities detected!")
        return

    # Group vulnerabilities by file (Ensuring no duplicates)
    file_vulnerabilities = {}
    for vuln in vulnerabilities:
        file_vulnerabilities.setdefault(vuln["file"], []).append(vuln)

    # Display file names (No duplicates)
    for file_name, issues in file_vulnerabilities.items():
        with st.expander(f"📄 {file_name} ({len(issues)} issues)"):
            for issue in issues:
                st.markdown(f"### 🔹 {issue['description']}")
                st.markdown(f"**Severity:** {issue['severity']}")
                st.code(issue["vulnerable_code"], language="python")

                # Show the "Fix Code" button **ONLY** for `.py` files
                if file_name.endswith(".py") and issue["recommended_fix"] != "No recommended fix provided.":
                    st.markdown("#### ✅ Recommended Fix:")
                    st.code(issue["recommended_fix"], language="python")

                    # Add Fix Code button with a unique key
                    if st.button(f"🛠️ Apply Fix - {file_name}:{issue['line']}", key=f"fix_{file_name}_{issue['line']}"):
                        apply_fix(issue)

                st.divider()

    # Display file names


import ast

def is_valid_python_code(code):
    """
    Check if a given string is valid Python code.
    Returns True if valid, False otherwise.
    """
    try:
        ast.parse(code)  # Try parsing the code
        return True
    except SyntaxError:
        return False