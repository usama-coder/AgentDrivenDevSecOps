from flask import Flask, request
from agents.vulnerability_agent import handle_vulnerability,  generate_markdown_report



def main():
    # Call handle_vulnerability to get the scan report
    issues = handle_vulnerability()

  #  Generate a Markdown report if there are any issues
    if issues:
        generate_markdown_report(issues)
    else:
        print("No vulnerabilities found.")

if __name__ == "__main__":
    main()