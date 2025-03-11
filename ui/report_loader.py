import re


def load_vulnerabilities(report_path="vulnerability_report.md"):
    """Parse vulnerabilities from the Markdown report."""
    vulnerabilities = []

    # Read the report
    try:
        with open(report_path, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        print(f"❌ Error: The report file '{report_path}' was not found.")
        return []

    # Split the content into individual vulnerability sections
    entries = content.split("----------------------------------------")

    for entry in entries:
        if not entry.strip():
            continue  # Skip empty sections

        # Extract file name and line number
        file_match = re.search(r"### File: (.*?), Line: (\d+)", entry)
        if not file_match:
            print("❌ Skipping entry - No file match found")
            continue

        file_name = file_match.group(1).strip()
        line_number = file_match.group(2).strip()

        # Extract description
        description_match = re.search(r"\*\*Description\*\*: (.*?)\n", entry, re.DOTALL)
        description = description_match.group(1).strip() if description_match else "No description provided."

        # Extract severity
        severity_match = re.search(r"\*\*Severity\*\*: (.*?)\n", entry, re.DOTALL)
        severity = severity_match.group(1).strip() if severity_match else "LOW"

        # Extract vulnerable code
        vulnerable_code_match = re.search(r"#### Vulnerable Code\n```python\n(.*?)```", entry, re.DOTALL)
        vulnerable_code = vulnerable_code_match.group(
            1).strip() if vulnerable_code_match else "No vulnerable code provided."

        # Extract recommended fix
        fix_match = re.search(r"#### Recommended Fix Code\n```python\n(.*?)```", entry, re.DOTALL)
        recommended_fix = fix_match.group(1).strip() if fix_match else "No recommended fix provided."

        # Extract recommendation description
        recommendation_match = re.search(r"#### Recommendation Description\n(.*?)\n", entry, re.DOTALL)
        recommendation_description = recommendation_match.group(
            1).strip() if recommendation_match else "No recommendation provided."

        # Append parsed vulnerability
        vulnerabilities.append({
            "file": file_name,
            "line": int(line_number),
            "description": description,
            "severity": severity,
            "vulnerable_code": vulnerable_code,
            "recommended_fix": recommended_fix,
            "recommendation_description": recommendation_description
        })

    print(f"✅ Extracted {len(vulnerabilities)} vulnerabilities successfully!")
    return vulnerabilities
