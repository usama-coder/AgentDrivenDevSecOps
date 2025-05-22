# Python Vulnerability Detection and Remediation Tool

This tool identifies vulnerabilities in Python code and provides actionable remediation recommendations. It uses a Large Language Model (LLM) to analyze the code, recommend fixes, and generate detailed Markdown reports.

## Features

- **Code Analysis**: Scans Python files for vulnerabilities.
- **LLM Integration**: Uses an LLM to provide precise and actionable recommendations for fixing vulnerabilities.
- **Markdown Reports**: Generates detailed reports highlighting:
  - Vulnerable code.
  - Recommended fixes.
  - Explanation of how the fix resolves the issue.
- **Supports Multiple Issues**: Handles multiple vulnerabilities in a single run.
- **Reflection**: Evaluates the quality of the output and adapts dynamically.

**Prerequisites**
Before running the tool, make sure you have the following installed:

Python 3.9+
pip (Python package manager)
Git (optional but recommended)
OpenAI API key for LLM-based features (e.g., remediation/fixes)

**Installation**
Clone this repository
Create a virtual environment (optional but recommended):
Install dependencies:
  pip install -r requirements.txt
Set Your OpenAI API Key  
  bash: export OPENAI_API_KEY=your-openai-api-key-here
  cmd set OPENAI_API_KEY=your-openai-api-key-here
Running the Tool
  python main.py

**Launch the Streamlit Dashboard**
bash :streamlit run dashboard.py


## 🚀 Security Dashboard
View the live dashboard here: [🔗https://devsecopsgit-79db8gxdtnxtgf4faurudv.streamlit.app/]
