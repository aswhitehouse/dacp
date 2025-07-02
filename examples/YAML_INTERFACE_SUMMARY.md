# YAML Configuration Interface for DACP Logging

## Overview

This document outlines the exact code interface you need to implement to use YAML-based configuration with DACP logging integration.

## Key Components

### 1. Configuration Loader

```python
from examples.yaml_config_interface import AgentConfigLoader

# Load YAML configuration
config = AgentConfigLoader.load_config("agent_config.yaml")

# Extract and process logging configuration
logging_config = AgentConfigLoader.extract_logging_config(config)
```

### 2. Base Configurable Agent

```python
from examples.yaml_config_interface import ConfigurableAgent

class MyAgent(ConfigurableAgent):
    def __init__(self, config_path=None):
        super().__init__(config_path=config_path)
        # Logging is automatically configured from YAML
        
    def _handle_capability(self, capability, message):
        # Override this method to implement your agent's specific capabilities
        if capability['name'] == 'my_task':
            return {"response": "Task completed"}
        return super()._handle_capability(capability, message)
```

### 3. Factory Function (Recommended)

```python
from examples.yaml_config_interface import create_agent_from_yaml

# One-liner to create fully configured agent
agent = create_agent_from_yaml("my_agent_config.yaml")
```

## YAML Configuration Format

```yaml
# agent_config.yaml
apiVersion: "v1"
kind: "Agent"
metadata:
  name: "my-agent"
  type: "smart_analysis"  # Used by factory to create appropriate class
  
# Logging configuration (automatically flows to DACP)
logging:
  enabled: true
  level: "INFO"                    # DEBUG, INFO, WARNING, ERROR, CRITICAL
  format_style: "emoji"            # emoji, detailed, simple
  include_timestamp: true
  log_file: "./logs/agent.log"
  
  # Environment variable overrides
  env_overrides:
    level: "DACP_LOG_LEVEL"
    format_style: "DACP_LOG_STYLE"
    log_file: "DACP_LOG_FILE"

# Intelligence configuration
intelligence:
  engine: "anthropic"
  model: "claude-3-haiku-20240618"
  api_key: "${ANTHROPIC_API_KEY}"  # Loaded from environment

# Agent capabilities (defines what tasks agent can handle)
capabilities:
  - name: "analyze_data"
    description: "Analyze datasets"
  - name: "generate_report"
    description: "Generate reports"
```

## Simple Usage Pattern

```python
import dacp
from examples.yaml_config_interface import create_agent_from_yaml

def main():
    # 1. Create agent from YAML (logging automatically configured)
    agent = create_agent_from_yaml("agent_config.yaml")
    
    # 2. Register with orchestrator
    orchestrator = dacp.Orchestrator()
    orchestrator.register_agent(agent.agent_metadata['name'], agent)
    
    # 3. Send messages (see logging in action)
    response = orchestrator.send_message(
        agent.agent_metadata['name'], 
        {"task": "analyze_data", "data": "sample data"}
    )
    print(response)
```

## What Happens Automatically

When you use this interface, the following happens automatically:

1. **YAML Loading**: Configuration file is parsed and validated
2. **Logging Setup**: DACP logging is configured with your specified settings
3. **Environment Integration**: Environment variables override YAML settings
4. **Directory Creation**: Log directories are created if needed
5. **Intelligence Config**: API keys are loaded from environment variables
6. **Agent Registration**: Agent capabilities are loaded from YAML
7. **Error Handling**: Comprehensive error handling and validation

## Environment Variable Overrides

You can override any YAML logging setting with environment variables:

```bash
export DACP_LOG_LEVEL=DEBUG
export DACP_LOG_STYLE=detailed
export DACP_LOG_FILE=./debug.log
export ANTHROPIC_API_KEY=your_api_key_here

python3 my_agent.py  # Uses environment overrides
```

## Integration with OAS Generator

For OAS generators, implement the `create_agent_from_yaml()` pattern:

```python
def generate_agent_code(oas_config):
    return f'''
import dacp
from yaml_config_interface import create_agent_from_yaml

def main():
    agent = create_agent_from_yaml("{oas_config}")
    orchestrator = dacp.Orchestrator()
    # ... rest of generated code
'''
```

This ensures every generated agent automatically gets:
- DACP logging integration
- YAML configuration support
- Environment variable overrides
- Error handling and validation 