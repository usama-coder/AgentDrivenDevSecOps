from langchain import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate

from logger import log_action

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
 recommended fix description:

{code}

Make sure the recommendations are Python-specific.
"""
prompt = PromptTemplate(template=remediation_template, input_variables=["code"])
remediation_chain = LLMChain(prompt=prompt, llm=llm)

# Reflection prompt template
reflection_template = """
You are an expert code reviewer. Your task is to evaluate the quality of the following remediation response generated for a vulnerable code snippet.

Remediation Response:
{response}

Evaluate the response based on the following criteria:
1. Does the response clearly identify the vulnerable code? (Yes/No)
2. Does the response provide a valid and secure fix? (Yes/No)
3. Is the fix concise and avoids unnecessary complexity? (Yes/No)
4. Is the explanation of the fix clear and sufficient? (Yes/No)

Provide feedback in the following format:
- Criteria 1: [Yes/No] - [Explanation]
- Criteria 2: [Yes/No] - [Explanation]
- Criteria 3: [Yes/No] - [Explanation]
- Criteria 4: [Yes/No] - [Explanation]

Overall, is the remediation response acceptable? (Yes/No)
"""
reflection_prompt = PromptTemplate(template=reflection_template, input_variables=["response"])
reflection_chain = LLMChain(prompt=reflection_prompt, llm=llm)


def reflect_with_llm(reflection_chain, response):
    """
    Use the reflection chain to evaluate the quality of the remediation response.
    """
    reflection_feedback = reflection_chain.run({"response": response})
    print("\nReflection Feedback:")
    print(reflection_feedback)

    overall_success = "Yes" in reflection_feedback.split("Overall, is the remediation response acceptable?")[-1]
    return {
        "overall_success": overall_success,
        "feedback": reflection_feedback
    }


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

        # Reflect on the remediation output using LLM
        reflections = reflect_with_llm(reflection_chain, filtered_response)

        # If the reflection indicates success, exit the retry loop
        if reflections["overall_success"]:
            print("Reflection indicates successful remediation.")
            break

        # If the reflection fails, refine the prompt for the next attempt
        print("Reflection indicates issues with the remediation. Adjusting workflow...")
        print(f"Feedback: {reflections['feedback']}")


        remediation_chain.prompt.template = """
        You are a Python security expert.Donot change any variable names, also return the response with the same variable name and keep the original letter casing. Review the following Python code for any vulnerabilities. 
        For each identified vulnerability, provide your response in the following format:

        Vulnerable Code:
        Recommended Fix:
        Recommended fix Description:

        Ensure that:
        1. The vulnerable code line is clearly identified.
        2. A specific recommended fix is provided.
        3. A concise explanation of why the fix resolves the issue is included.

        Code:
        {code}
        """
        print("Updated prompt with more specific instructions.")


        filtered_response = "Remediation unsuccessful. Please review manually."

    return filtered_response


import re


def extract_function_from_file(file_path, line_number):
    """Extract the function that contains the specified line number."""
    print(f"/nextracting func from file:{file_path} and line {line_number} ")
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    start_idx, end_idx = None, None

    # Find function start
    for i in range(line_number - 1, -1, -1):
        if lines[i].strip().startswith("def "):
            start_idx = i
            break

    # Find function end (next function, class, or EOF)
    for i in range(line_number, len(lines)):
        if lines[i].strip().startswith(("def ", "class ")):
            end_idx = i
            break

    if start_idx is None:
        print("⚠️ Could not locate function start.")
        return None

    if end_idx is None:
        end_idx = len(lines)

    return lines[start_idx:end_idx]

def llm_replace_vulnerability(function_code, vulnerability, recommended_fix):

    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.3)

    prompt = PromptTemplate(template="""
    You are a security expert. Your task is to **fix the vulnerability** in the following Python function.

    **Vulnerability:** {vulnerability}

    **Recommended Fix:** {recommended_fix}

    **Original Function:**
    ```python
    {function_code}
    ```

    **Instructions:**
    - Identify the vulnerable line and **replace it** with the recommended fix .
    - Keep the **original function structure** and indentation unchanged.
    - Do not introduce unnecessary changes.


    Return **only** the corrected function code:
    """, input_variables=["function_code", "vulnerability", "recommended_fix"])

    fixing_chain = LLMChain(prompt=prompt, llm=llm)

    return fixing_chain.run({
        "function_code": "".join(function_code),
        "vulnerability": vulnerability,
        "recommended_fix": recommended_fix
    })

def overwrite_function_in_file(file_path, old_function, new_function):

    with open(file_path, "r", encoding="utf-8") as f:
        file_content = f.read()

    old_func_str = "".join(old_function).strip()
    new_func_str = clean_fix(new_function.strip())
    updated_content = file_content.replace(old_func_str, new_func_str)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(updated_content)

    print("✅ Code Fix Applied Successfully!")
def clean_fix(recommended_fix):

    cleaned_fix = re.sub(r"```[a-zA-Z]*\n?", "", recommended_fix)
    cleaned_fix = cleaned_fix.strip()
    return cleaned_fix.strip()