import json

def parse_agent_response(response: str | dict) -> dict:
    """
    Parse the agent/LLM response (as string or dict) and return a dict.
    """
    if isinstance(response, dict):
        return response
    try:
        return json.loads(response)
    except Exception as e:
        raise ValueError(f"Malformed agent response: {e}")

def is_tool_request(msg: dict) -> bool:
    return "tool_request" in msg

def get_tool_request(msg: dict) -> tuple[str, dict]:
    req = msg["tool_request"]
    return req["name"], req.get("args", {})

def wrap_tool_result(name: str, result: dict) -> dict:
    return {"tool_result": {"name": name, "result": result}}

def is_final_response(msg: dict) -> bool:
    return "final_response" in msg

def get_final_response(msg: dict) -> dict:
    return msg["final_response"]
