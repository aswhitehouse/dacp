# DACP - Declarative Agent Communication Protocol

A Python library for managing LLM/agent communications and tool function calls following the OAS Open Agent Specification.

## Installation

```bash
pip install -e .
```

## Quick Start

```python
import dacp

# Create an orchestrator to manage agents
orchestrator = dacp.Orchestrator()

# Create and register an agent
class MyAgent:
    def handle_message(self, message):
        return {"response": f"Hello {message.get('name', 'World')}!"}

agent = MyAgent()
orchestrator.register_agent("my-agent", agent)

# Send a message to the agent
response = orchestrator.send_message("my-agent", {"name": "Alice"})
print(response)  # {"response": "Hello Alice!"}

# Use built-in tools
result = dacp.file_writer("./output/greeting.txt", "Hello, World!")
print(result["message"])  # "Successfully wrote 13 characters to ./output/greeting.txt"

# Call an LLM directly
response = dacp.call_llm("What is the weather like today?")
```

## Features

- **Agent Orchestration**: Central management of multiple agents with message routing
- **Tool Registry**: Register and manage custom tools for LLM agents
- **Built-in Tools**: Includes a `file_writer` tool that automatically creates parent directories
- **LLM Integration**: Built-in support for OpenAI models (extensible)
- **Protocol Parsing**: Parse and validate agent responses
- **Tool Execution**: Safe execution of registered tools
- **Conversation History**: Track and query agent interactions
- **OAS Compliance**: Follows Open Agent Specification standards

## API Reference

### Orchestrator

- `Orchestrator()`: Create a new orchestrator instance
- `register_agent(agent_id: str, agent) -> None`: Register an agent
- `unregister_agent(agent_id: str) -> bool`: Remove an agent
- `send_message(agent_id: str, message: Dict) -> Dict`: Send message to specific agent
- `broadcast_message(message: Dict, exclude_agents: List[str] = None) -> Dict`: Send message to all agents
- `get_conversation_history(agent_id: str = None) -> List[Dict]`: Get conversation history
- `clear_history() -> None`: Clear conversation history
- `get_session_info() -> Dict`: Get current session information

### Tools

- `register_tool(tool_id: str, func)`: Register a new tool
- `run_tool(tool_id: str, args: Dict) -> dict`: Execute a registered tool
- `TOOL_REGISTRY`: Access the current tool registry
- `file_writer(path: str, content: str) -> dict`: Write content to file, creating directories automatically

### LLM

- `call_llm(prompt: str, model: str = "gpt-4") -> str`: Call an LLM with a prompt

### Protocol

- `parse_agent_response(response: str | dict) -> dict`: Parse agent response
- `is_tool_request(msg: dict) -> bool`: Check if message is a tool request
- `get_tool_request(msg: dict) -> tuple[str, dict]`: Extract tool request details
- `wrap_tool_result(name: str, result: dict) -> dict`: Wrap tool result for agent
- `is_final_response(msg: dict) -> bool`: Check if message is a final response
- `get_final_response(msg: dict) -> dict`: Extract final response

## Agent Development

### Creating an Agent

Agents must implement a `handle_message` method:

```python
import dacp

class GreetingAgent:
    def handle_message(self, message):
        name = message.get("name", "World")
        task = message.get("task")
        
        if task == "greet":
            return {"response": f"Hello, {name}!"}
        elif task == "farewell":
            return {"response": f"Goodbye, {name}!"}
        else:
            return {"error": f"Unknown task: {task}"}

# Register the agent
orchestrator = dacp.Orchestrator()
agent = GreetingAgent()
orchestrator.register_agent("greeter", agent)

# Use the agent
response = orchestrator.send_message("greeter", {
    "task": "greet", 
    "name": "Alice"
})
print(response)  # {"response": "Hello, Alice!"}
```

### Agent Base Class

You can also inherit from the `Agent` base class:

```python
import dacp

class MyAgent(dacp.Agent):
    def handle_message(self, message):
        return {"processed": message}
```

### Tool Requests from Agents

Agents can request tool execution by returning properly formatted responses:

```python
class ToolUsingAgent:
    def handle_message(self, message):
        if message.get("task") == "write_file":
            return {
                "tool_request": {
                    "name": "file_writer",
                    "args": {
                        "path": "./output/agent_file.txt",
                        "content": "Hello from agent!"
                    }
                }
            }
        return {"response": "Task completed"}

# The orchestrator will automatically execute the tool and return results
orchestrator = dacp.Orchestrator()
agent = ToolUsingAgent()
orchestrator.register_agent("file-agent", agent)

response = orchestrator.send_message("file-agent", {"task": "write_file"})
# Tool will be executed automatically
```

## Built-in Tools

### file_writer

The `file_writer` tool automatically creates parent directories and writes content to files:

```python
import dacp

# This will create the ./output/ directory if it doesn't exist
result = dacp.file_writer("./output/file.txt", "Hello, World!")

if result["success"]:
    print(f"File written: {result['path']}")
    print(f"Message: {result['message']}")
else:
    print(f"Error: {result['error']}")
```

**Features:**
- ✅ Automatically creates parent directories
- ✅ Handles Unicode content properly
- ✅ Returns detailed success/error information
- ✅ Safe error handling

## Development

```bash
# Install development dependencies
pip install -e .[dev]

# Run tests
pytest

# Format code
black .

# Lint code
flake8
```

## License

MIT License
