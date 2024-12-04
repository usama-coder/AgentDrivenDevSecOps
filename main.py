
from agents.vulnerability_agent import handle_vulnerability,  generate_markdown_report



def main():
    # Call handle_vulnerability to get the scan report
    issues = handle_vulnerability()
    issues = [issue for issue in issues if issue]
  #  Generate a Markdown report if there are any issues
    if not issues:
        print("No vulnerabilities found.")

    else:
        generate_markdown_report(issues)

if __name__ == "__main__":
    main()