from langchain import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate

# Initialize the LLM
llm = ChatOpenAI(model="gpt-4")

remediation_template = """
You are a Python security expert. Review the following Python code for any security vulnerabilities and provide specific code fixes. 
Only include the code fixes with the format:
- Vulnerable Code:
- Recommended Fix:

{code}

Make sure the recommendations are Python-specific and relevant to common security issues like injection attacks, unsafe function usage, or improper input handling.
"""


prompt = PromptTemplate(template=remediation_template, input_variables=["code"])
remediation_chain = LLMChain(prompt=prompt, llm=llm)

def filter_response(response):
    sections = []
    in_code_block = False
    current_section = None

    for line in response.splitlines():
        if line.startswith("- Vulnerable Code:"):
            current_section = {"Vulnerable Code": line}
            sections.append(current_section)
        elif line.startswith("- Recommended Fix:"):
            current_section["Recommended Fix"] = line

        # Add lines to current section if they are code
        elif current_section and (line.startswith("```") or line.strip()):
            current_section[list(current_section.keys())[-1]] += f"\n{line}"

    # Format the output
    formatted_response = ""
    for section in sections:
        vulnerable_code = section.get("Vulnerable Code", "").replace("- Vulnerable Code:", "Vulnerable Code:")
        recommended_fix = section.get("Recommended Fix", "").replace("- Recommended Fix:", "Recommended Fix:")
        formatted_response += f"{vulnerable_code}\n\n{recommended_fix}\n\n{'-'*40}\n"

    return formatted_response.strip()

def run_remediation_chain(vulnerable_code):
    response = remediation_chain.run({"code": vulnerable_code})
    filtered_response = filter_response(response)
    print("Filtered Code Fixes and Recommendations:")
    print(filtered_response)
    return filtered_response
