from logger import log_action

def reflect_on_remediation_process(response, criteria):
    """
    Reflect on the output of the remediation process.
    Evaluate based on the criteria provided.
    """
    success_criteria = {
        "contains_vulnerable_code": "Vulnerable Code" in response,
        "contains_recommended_fix": "Recommended Fix" in response,
        "contains_description": "Recommended fix Description" in response,
    }

    # Evaluate against user-defined criteria
    success_criteria.update(criteria)

    # Summarize reflections
    observations = {
        "overall_success": all(success_criteria.values()),
        "detailed_criteria": success_criteria,
    }

    # Log the reflection for future use
    log_action(
        agent_name="LLMRemediationAgent",
        action="Reflection",
        input_data={"response": response},
        output_data=observations,
    )

    return observations
