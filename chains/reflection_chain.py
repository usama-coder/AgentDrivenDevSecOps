from langchain.prompts import PromptTemplate
from langchain import LLMChain

# Define the reflection prompt
reflection_prompt = PromptTemplate(
    template="""
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
    """,
    input_variables=["response"]
)

# Initialize the reflection chain
reflection_chain = LLMChain(llm=llm, prompt=reflection_prompt)
