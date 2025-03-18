
from langchain.prompts import PromptTemplate

# Prompt for remediation suggestions
REMEDIATION_PROMPT = PromptTemplate(
    template="""
    You are a Python security expert. Review the following Python code for vulnerabilities and provide specific code fixes.
    Format:
    Vulnerable Code:
    Recommended Fix:
    Recommended Fix Description:

    Code:
    {code}
    """,
    input_variables=["code"]
)

REMEDIATION_RETRY_PROMPT = PromptTemplate(
    template="""
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
    """,
    input_variables=["code"]
)

# Prompt for reflecting on remediation output
REFLECTION_PROMPT = PromptTemplate(
    template="""
    You are a Python security expert tasked with evaluating the quality of the following output.
    Please answer the following:
    1. Did you identify all vulnerabilities in the code?
    2. Are the recommendations specific and actionable?
    3. Is the explanation clear and concise?
    4. Does the output adhere to the required format?

    Output:
    {output}

    Provide your evaluation in the following format:
    Reflection:
    1. [Yes/No/Partially]: ...
    2. [Yes/No/Partially]: ...
    3. [Yes/No/Partially]: ...
    4. [Yes/No/Partially]: ...
    """,
    input_variables=["output"]
)
