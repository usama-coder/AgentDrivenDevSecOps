
from agents.vulnerability_agent import handle_vulnerability,  generate_markdown_report



def main():

    issues = handle_vulnerability()
    if isinstance(issues, dict) and not issues.get("issues"):
        print("No vulnerabilities found.")
    else:
        generate_markdown_report(issues)

if __name__ == "__main__":
    main()