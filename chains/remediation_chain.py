from langchain import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from logger import log_action
from reflection import reflect_on_remediation_process
import os

# Initialize the LLM
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.7,
    openai_api_key="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",
)

remediation_template = """
You are a Python security expert. Review the following Python code for any security vulnerabilities and provide specific code fixes and only give to the point and precise description. Ignore all the imports and don't give code from importing till end, just give the fix for the line which has vulnerability.ensure the response length is less than 500 
Only include the code fixes with the format:
 Vulnerable Code:
 Recommended Fix:
\n\n Recommended fix Description:

{code}

Make sure the recommendations are Python-specific.
"""
prompt = PromptTemplate(template=remediation_template, input_variables=["code"])
remediation_chain = LLMChain(prompt=prompt, llm=llm)


def filter_response(response):
    """Filter and format the LLM response to include only relevant information."""
    sections = []
    current_section = None

    for line in response.splitlines():
        if line.startswith("Vulnerable Code:"):
            current_section = {"Vulnerable Code": line}
            sections.append(current_section)
        elif line.startswith("Recommended Fix:"):
            current_section["Recommended Fix"] = line

        # Add lines to current section if they are code
        elif current_section and (line.startswith("```") or line.strip()):
            current_section[list(current_section.keys())[-1]] += f"\n{line}"

    # Process each section to include only modified lines within the "Recommended Fix" section
    formatted_response = ""
    for section in sections:
        vulnerable_code = section.get("Vulnerable Code", "").replace("- Vulnerable Code:", "Vulnerable Code:")
        recommended_fix = section.get("Recommended Fix", "").replace("- Recommended Fix:", "Recommended Fix:")

        # Filter out any lines that start with imports (e.g., "import") in the recommended fix
        filtered_fix_lines = [
            line for line in recommended_fix.splitlines()
            if not line.strip().startswith("import") and line.strip()
        ]

        # Rebuild the "Recommended Fix" section with only relevant lines
        filtered_recommended_fix = "\n".join(filtered_fix_lines)

        formatted_response += f"{vulnerable_code}\n\n{filtered_recommended_fix}\n\n{'-' * 40}\n"

    return formatted_response.strip()


def run_remediation_chain(vulnerable_code):
    """Run the LLM remediation chain, reflect on its output, and adapt."""
    max_attempts = 2
    attempt = 0
    reflections = None
    response = None
    filtered_response = None

    while attempt < max_attempts:
        attempt += 1
        print(f"\nAttempt {attempt}: Running the remediation chain...")

        # Generate remediation suggestions
        response = remediation_chain.run({"code": vulnerable_code})
        filtered_response = filter_response(response)

        print("\nFiltered Code Fixes and Recommendations:")
        print(filtered_response)

        # Log the input and output of the remediation chain
        log_action(
            agent_name="LLMRemediationAgent",
            action="Generate Remediation",
            input_data={"code": vulnerable_code},
            output_data={"response": response},
        )

        # Reflect on the remediation output
        reflection_criteria = {
            "fix_length_reasonable": len(filtered_response) < 900
        }
        reflections = reflect_on_remediation_process(filtered_response, reflection_criteria)

        # If the reflection indicates success, exit the retry loop
        if reflections["overall_success"]:
            print("Reflection indicates successful remediation.")
            break

        # If the reflection fails, refine the prompt for the next attempt
        print("Reflection indicates issues with the remediation. Adjusting workflow...")
        failed_criteria = [
            key for key, value in reflections["detailed_criteria"].items() if not value
        ]
        print(f"Failed criteria: {failed_criteria}")

        # Log the failed criteria
        log_action(
            agent_name="LLMRemediationAgent",
            action="Reflection Failure",
            input_data={"code": vulnerable_code},
            output_data={"failed_criteria": failed_criteria, "response": response},
        )

        # Adjust the prompt based on reflection
        new_prompt = """
      You are a Python security expert. Review the following Python code for any vulnerabilities. For each identified vulnerability, provide your response in the following format:

 Vulnerable Code:
 Recommended Fix:
 Recommended fix Description:

 Ensure that:
 1. The vulnerable code line is clearly identified.
 2. A specific recommended fix is provided.
 3. A concise explanation of why the fix resolves the issue is included.

 Focus on providing actionable and clear recommendations.

 Code:
 {code}
"""
        remediation_chain.prompt.template = new_prompt
        print("Updated prompt with more specific instructions.")

    # If all attempts fail, log and provide fallback
    if not reflections or not reflections["overall_success"]:
        print("All remediation attempts failed. Proceeding with fallback workflow...")
        log_action(
            agent_name="LLMRemediationAgent",
            action="Fallback",
            input_data={"code": vulnerable_code},
            output_data={"reason": "Incomplete remediation after retries"},
        )
        filtered_response = "Remediation unsuccessful. Please review manually."

    return filtered_response

