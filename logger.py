import json
import datetime

def log_action(agent_name, action, input_data, output_data):
    """Log an agent's action and reflection."""
    log_entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "agent_name": agent_name,
        "action": action,
        "input": input_data,
        "output": output_data,
    }
    with open("agent_logs.json", "a") as log_file:
        log_file.write(json.dumps(log_entry) + "\n")
