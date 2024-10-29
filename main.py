from flask import Flask, request
from agents.vulnerability_agent import handle_vulnerability,  generate_markdown_report



def main():
    # Call handle_vulnerability to get the scan report
    report = handle_vulnerability()

    # Generate a Markdown report if there are any issues
    if report['issues']:
        generate_markdown_report(report['issues'])
    else:
        print("No vulnerabilities found.")

if __name__ == "__main__":
    main()