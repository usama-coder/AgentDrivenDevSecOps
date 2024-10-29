import subprocess

def run_snyk_scan():
    try:
        result = subprocess.run(['snyk', 'test'], capture_output=True, text=True)
        if result.returncode == 0:
            print("No vulnerabilities found.")
            return {"issues": []}  # Return an empty report if no issues
        else:
            # Process and return the report as JSON
            return {"issues": parse_snyk_output(result.stdout)}
    except Exception as e:
        print(f"Error running scan: {e}")
        return {"issues": []}

def parse_snyk_output(output):
    # Basic parsing logic to extract issues
    # Customize this to parse specific details from Snyk output
    issues = []
    for line in output.split("\n"):
        if "Vulnerability" in line:
            issues.append({"title": line, "code": "Example code snippet"})
    return issues
