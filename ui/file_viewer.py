import re
import streamlit as st
import ast
import requests
import base64

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
        # overwrite_function_in_file(file_name, extracted_function, fixed_function)
        update_github_file(file_name, fixed_function,extracted_function)

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


def is_valid_python_code(code):
    try:
        ast.parse(code)
        return True
    except SyntaxError:
        return False


def update_github_file(file_path, fixed_function,original_function):
    """Update a file in a GitHub repository after applying the fix."""
    GITHUB_TOKEN = st.secrets["GITHUB_TOKEN"]
    REPO_OWNER = st.secrets["REPO_OWNER"]
    REPO_NAME = st.secrets["REPO_NAME"]
    GITHUB_BRANCH = st.secrets["GITHUB_BRANCH"]

    # GitHub API URL for the file
    file_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{file_path}"

    # Get current file content
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}

    # Get current file content
    response = requests.get(file_url, headers=headers)

    if response.status_code == 200:
        file_data = response.json()
        sha = file_data["sha"]  # Required for updating the file
        current_content = base64.b64decode(file_data["content"]).decode("utf-8")
        fixed_function=clean_fix(fixed_function)
        # Replace only the vulnerable function, keeping the rest of the file unchanged
        if original_function in current_content:
            updated_content = current_content.replace(original_function, fixed_function)
        else:
            st.error(f"⚠️ Could not find the function in {file_path}. No changes made.")
            return

        # Prepare the request payload
        payload = {
            "message": f"🚀 Auto-fix applied to {file_path}",
            "content": base64.b64encode(updated_content.encode()).decode("utf-8"),
            "sha": sha,
            "branch": GITHUB_BRANCH
        }

        # Send request to update file
        update_response = requests.put(file_url, headers=headers, json=payload)

        if update_response.status_code == 200:
            st.success(f"✅ Fix successfully applied and pushed to GitHub: {file_path}")
        else:
            st.error(f"❌ Failed to update {file_path} on GitHub! Error: {update_response.text}")

    else:
        st.error(f"❌ Could not fetch {file_path} from GitHub. Error: {response.text}")


def clean_fix(recommended_fix):

    cleaned_fix = re.sub(r"```[a-zA-Z]*\n?", "", recommended_fix)
    cleaned_fix = cleaned_fix.strip()
    return cleaned_fix.strip()