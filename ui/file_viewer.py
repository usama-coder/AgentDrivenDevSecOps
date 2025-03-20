import re
import streamlit as st
import ast
import requests
import base64
import hashlib

from chains.remediation_chain import (
    extract_function_from_file,
    llm_replace_vulnerability,
    overwrite_function_in_file
)
def clean_recommended_fix(recommended_fix):
    """Remove markdown code block formatting from the recommended fix."""
    return re.sub(r"```[a-zA-Z]*\n?", "", recommended_fix).strip()


def apply_fix(issue):
    """Apply the LLM-recommended fix to the vulnerable file."""
    file_name = issue["file"]
    line_number = issue["line"]
    recommended_fix = clean_recommended_fix(issue["recommended_fix"])

    if "selected_pr_branch" not in st.session_state or not st.session_state["selected_pr_branch"]:
        st.error("❌ No source branch selected! Please select a PR before applying fixes.")
        return

    extracted_function = extract_function_from_file(file_name, line_number)

    if not is_valid_python_code(recommended_fix):
        st.warning(f"⚠️ The recommended fix for `{file_name}` at line `{line_number}` is not valid Python code.")
        st.markdown("### Suggested Manual Fix:")
        st.code(issue["recommended_fix"], language="python")
        return

    if extracted_function:
        fixed_function = llm_replace_vulnerability(
            extracted_function, issue["vulnerable_code"], recommended_fix
        )

        update_github_file(file_name, fixed_function, extracted_function)
        st.success(
            f"✅ LLM Applied Fix to `{file_name}` at Line {line_number} (Branch: `{st.session_state['selected_pr_branch']}`)!"
        )
    else:
        st.error("⚠️ Could not find the function to fix in the provided file and line number.")


def render_file_viewer(vulnerabilities):
    """Render vulnerabilities grouped by file with fix options."""
    if not vulnerabilities:
        st.success("✅ No vulnerabilities detected!")
        return

    st.subheader("📂 Vulnerabilities by File")
    st.markdown("""
        - Click on a file in the **detailed view** to explore specific vulnerabilities and suggested fixes.        
    """)

    # Track highest severity for each file
    file_vulnerabilities = {}
    file_severity = {}

    for vuln in vulnerabilities:
        file_vulnerabilities.setdefault(vuln["file"], []).append(vuln)
        severity = vuln["severity"].upper()

        # Store highest severity for each file
        if vuln["file"] not in file_severity or severity in ["HIGH", "MEDIUM"]:
            file_severity[vuln["file"]] = severity

    # Define severity color labels
    severity_colors = {
        "HIGH": "🔴",
        "MEDIUM": "🟠",
        "LOW": "🟢"
    }

    for file_name, issues in file_vulnerabilities.items():
        severity_label = severity_colors.get(file_severity[file_name], "⚪")
        with st.expander(f"{severity_label} 📄 {file_name} ({len(issues)} issues)"):
            for index, issue in enumerate(issues):
                st.markdown(f"### 🔹 {issue['description']}")
                st.markdown(f"**Severity:** {issue['severity']}")
                st.code(issue["vulnerable_code"], language="python")

                if file_name.endswith(".py") and issue["recommended_fix"] != "No recommended fix provided.":
                    st.markdown("#### ✅ Recommended Fix:")
                    st.code(issue["recommended_fix"], language="python")

                    # Generate a unique key for session state tracking
                    unique_id = hashlib.sha256(f"{file_name}_{issue['line']}_{index}".encode()).hexdigest()
                    fix_key = f"fix_applied_{unique_id}"

                    # If the fix is applied, disable the button
                    if st.session_state.get(fix_key, False):
                        st.button(f"✅ Fix Applied - {file_name}:{issue['line']}", disabled=True, key=f"fixed_{unique_id}")
                    else:
                        if st.button(f"🛠️ Apply Fix - {file_name}:{issue['line']}", key=f"fix_{unique_id}"):
                            apply_fix(issue)
                            st.session_state[fix_key] = True  # ✅ Mark fix as applied

                st.divider()


def is_valid_python_code(code):
    """Check if the provided code is valid Python."""
    try:
        ast.parse(code)
        return True
    except SyntaxError:
        return False


def update_github_file(file_path, fixed_function, original_function):
    """Update the given file on GitHub with the fixed function."""
    GITHUB_TOKEN = st.secrets["GITHUB_TOKEN"]
    REPO_OWNER = st.secrets["REPO_OWNER"]
    REPO_NAME = st.secrets["REPO_NAME"]

    if "selected_pr_branch" not in st.session_state or not st.session_state["selected_pr_branch"]:
        st.error("❌ No source branch found for this PR!")
        return

    GITHUB_BRANCH = st.session_state["selected_pr_branch"]

    file_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{file_path}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}

    response = requests.get(file_url, headers=headers, params={"ref": GITHUB_BRANCH})

    if response.status_code == 200:
        file_data = response.json()
        sha = file_data["sha"]
        current_content = base64.b64decode(file_data["content"]).decode("utf-8")
        fixed_function = clean_fix(fixed_function)

        if isinstance(original_function, list):
            original_function = "\n".join(original_function)

        if original_function in current_content:
            updated_content = current_content.replace(original_function, fixed_function)
        else:
            st.error(f"⚠️ Could not find the function in `{file_path}`. No changes made.")
            return

        payload = {
            "message": f"Auto-fix applied to {file_path}",
            "content": base64.b64encode(updated_content.encode()).decode("utf-8"),
            "sha": sha,
            "branch": GITHUB_BRANCH
        }

        update_response = requests.put(file_url, headers=headers, json=payload)

        if update_response.status_code == 200:
            st.success(f"✅ Fix successfully applied and pushed to GitHub: `{file_path}`")
        else:
            st.error(f"❌ Failed to update `{file_path}` on GitHub! Error: {update_response.text}")

    else:
        st.error(f"❌ Could not fetch `{file_path}` from GitHub. Error: {response.text}")


def clean_fix(recommended_fix):
    """Clean recommended fix code by removing unnecessary formatting."""
    return re.sub(r"```[a-zA-Z]*\n?", "", recommended_fix).strip()
