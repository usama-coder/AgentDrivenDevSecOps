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
    cleaned_fix = re.sub(r"```[a-zA-Z]*\n?", "", recommended_fix)
    cleaned_fix = cleaned_fix.strip()
    return cleaned_fix.strip()


def apply_fix(issue):
    file_name = issue["file"]
    line_number = issue["line"]
    recommended_fix = clean_recommended_fix(issue["recommended_fix"])

    if "selected_pr_branch" not in st.session_state or not st.session_state["selected_pr_branch"]:
        st.error("❌ No source branch selected! Please select a PR before applying fixes.")
        return

    extracted_function = extract_function_from_file(file_name, line_number)

    if not is_valid_python_code(recommended_fix):
        st.warning(
            f"⚠️ The recommended fix for `{file_name}` at line `{line_number}` is not a direct code replacement.")
        st.markdown("### Suggested Manual Fix:")
        st.info(issue["recommended_fix"])
        return

    if extracted_function:
        fixed_function = llm_replace_vulnerability(
            extracted_function, issue["vulnerable_code"], recommended_fix        )

        update_github_file(file_name, fixed_function, extracted_function)
        st.success(
            f"✅ LLM Applied Fix to {file_name} at Line {line_number} (Branch: {st.session_state['selected_pr_branch']})!")
    else:
        st.error("⚠️ Could not find the function to fix.")


def render_file_viewer(vulnerabilities):
    if not vulnerabilities:
        st.info("✅ No vulnerabilities detected!")
        return

    file_vulnerabilities = {}
    for vuln in vulnerabilities:
        file_vulnerabilities.setdefault(vuln["file"], []).append(vuln)

    for file_name, issues in file_vulnerabilities.items():
        with st.expander(f"📄 {file_name} ({len(issues)} issues)"):
            for index, issue in enumerate(issues):
                st.markdown(f"### 🔹 {issue['description']}")
                st.markdown(f"**Severity:** {issue['severity']}")
                st.code(issue["vulnerable_code"], language="python")

                if file_name.endswith(".py") and issue["recommended_fix"] != "No recommended fix provided.":
                    st.markdown("#### ✅ Recommended Fix:")
                    st.code(issue["recommended_fix"], language="python")
                    st.markdown("#### ✅ Recommended Fix Description:")
                    st.markdown(issue["description"])
                    # 🔹 Ensure the button key is unique using a hash
                    unique_id = hashlib.sha256(f"{file_name}_{issue['line']}_{index}".encode()).hexdigest()
                    if st.button(f"🛠️ Apply Fix - {file_name}:{issue['line']}", key=f"fix_{unique_id}"):
                        apply_fix(issue)

                st.divider()


def is_valid_python_code(code):
    try:
        ast.parse(code)
        return True
    except SyntaxError:
        return False


def update_github_file(file_path, fixed_function, original_function):
    GITHUB_TOKEN = st.secrets["GITHUB_TOKEN"]
    REPO_OWNER = st.secrets["REPO_OWNER"]
    REPO_NAME = st.secrets["REPO_NAME"]

    if "selected_pr_branch" not in st.session_state or not st.session_state["selected_pr_branch"]:
        st.error("❌ No source branch found for this PR!")
        return

    GITHUB_BRANCH = st.session_state["selected_pr_branch"]  # Dynamically set the branch
    file_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{file_path}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}

    response = requests.get(file_url, headers=headers, params={"ref": GITHUB_BRANCH})

    if response.status_code == 200:
        file_data = response.json()
        sha = file_data["sha"]
        current_content = base64.b64decode(file_data["content"]).decode("utf-8")
        fixed_function= clean_fix(fixed_function)

        if isinstance(original_function, list):
            original_function = "\n".join(original_function)

        if original_function in current_content:
            updated_content = current_content.replace(original_function, fixed_function)
        else:
            st.error(f"⚠️ Could not find the function in {file_path}. No changes made.")
            return

        payload = {
            "message": f" Auto-fix applied to {file_path}",
            "content": base64.b64encode(updated_content.encode()).decode("utf-8"),
            "sha": sha,
            "branch": GITHUB_BRANCH
        }

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