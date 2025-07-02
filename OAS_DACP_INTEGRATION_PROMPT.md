# OAS Integration with DACP Logging - Implementation Guide

## Overview

This document provides a complete implementation guide for integrating DACP (Declarative Agent Communication Protocol) logging capabilities into the Open Agent Spec (OAS) project. This integration will enable automatic logging configuration and comprehensive observability for all generated agents.

## Background

DACP is a Python package that provides:
- Multi-provider LLM integration (OpenAI, Anthropic, Azure, Local)
- Comprehensive logging and observability
- Agent orchestration framework
- Tool execution capabilities

The goal is to integrate DACP's logging system into OAS so that generated agents automatically have comprehensive logging with zero boilerplate code.

## YAML Configuration Additions

### 1. Add Logging Section to OAS YAML Schema

Add this new section to your OAS YAML specification:

```yaml
# agent_config.yaml
apiVersion: "v1"
kind: "Agent"
metadata:
  name: "my-agent"
  version: "1.0.0"
  type: "analysis_agent"  # Used by generator to select agent class template

# EXISTING SECTIONS (intelligence, capabilities, etc.)
intelligence:
  engine: "anthropic"
  model: "claude-3-haiku-20240618"
  # ... existing intelligence config

# NEW: DACP Logging Configuration Section
logging:
  enabled: true                    # Whether to enable DACP logging
  level: "INFO"                    # DEBUG, INFO, WARNING, ERROR, CRITICAL
  format_style: "emoji"            # emoji, detailed, simple
  include_timestamp: true          # Include timestamps in log messages
  log_file: "./logs/agent.log"     # Optional: log to file (creates directories)
  
  # Environment variable overrides (allows runtime configuration)
  env_overrides:
    level: "DACP_LOG_LEVEL"        # env var name that overrides level
    format_style: "DACP_LOG_STYLE" # env var name that overrides format_style
    log_file: "DACP_LOG_FILE"      # env var name that overrides log_file

# EXISTING SECTIONS CONTINUE...
capabilities:
  - name: "analyze_data"
    description: "Analyze datasets"
  # ... rest of existing config
```

### 2. Schema Validation Rules

Add these validation rules to your OAS schema:

```yaml
# Schema additions for logging section
logging:
  type: object
  properties:
    enabled:
      type: boolean
      default: true
    level:
      type: string
      enum: ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
      default: "INFO"
    format_style:
      type: string
      enum: ["emoji", "detailed", "simple"]
      default: "emoji"
    include_timestamp:
      type: boolean
      default: true
    log_file:
      type: string
      description: "Path to log file (optional)"
    env_overrides:
      type: object
      properties:
        level:
          type: string
          description: "Environment variable name for level override"
        format_style:
          type: string
          description: "Environment variable name for format_style override"
        log_file:
          type: string
          description: "Environment variable name for log_file override"
```

## Code Generation Requirements

### 1. Dependencies

Generated agents must include these dependencies:

```python
# At top of generated agent file
import os
import logging
from pathlib import Path
from typing import Dict, Any, Optional
import dacp  # Main DACP package
```

### 2. Configuration Loading Class

Generate this class in each agent (or import from a shared module):

```python
class AgentConfigLoader:
    """Handles loading and processing agent configuration from YAML files."""
    
    @staticmethod
    def extract_logging_config(config: Dict[str, Any]) -> Dict[str, Any]:
        """Extract and process logging configuration for DACP."""
        logging_config = config.get('logging', {})
        
        if not logging_config.get('enabled', True):
            return {'enabled': False}
        
        env_overrides = logging_config.get('env_overrides', {})
        processed_config = {}
        
        # Process each parameter with environment variable fallback
        level = logging_config.get('level', 'INFO')
        if 'level' in env_overrides:
            level = os.getenv(env_overrides['level'], level)
        processed_config['level'] = level
        
        format_style = logging_config.get('format_style', 'emoji')
        if 'format_style' in env_overrides:
            format_style = os.getenv(env_overrides['format_style'], format_style)
        processed_config['format_style'] = format_style
        
        log_file = logging_config.get('log_file')
        if 'log_file' in env_overrides:
            log_file = os.getenv(env_overrides['log_file'], log_file)
        
        if log_file:
            # Ensure log directory exists
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)
            processed_config['log_file'] = str(log_path)
        
        processed_config['include_timestamp'] = logging_config.get('include_timestamp', True)
        processed_config['enabled'] = True
        
        return processed_config
```

### 3. Base Agent Class

Generate agents that extend this base class:

```python
class {AgentClassName}(dacp.Agent):
    """Generated agent with DACP logging integration."""
    
    def __init__(self):
        """Initialize agent with automatic logging configuration."""
        # Load the configuration that was embedded during generation
        self.config = {
            # YAML config embedded here during generation
            "metadata": {metadata_from_yaml},
            "logging": {logging_config_from_yaml},
            "intelligence": {intelligence_config_from_yaml},
            "capabilities": {capabilities_from_yaml}
        }
        
        # Setup logging FIRST (before any other DACP operations)
        self.setup_logging()
        
        # Initialize other components
        self.intelligence_config = self._load_intelligence_config()
        self.agent_metadata = self.config.get('metadata', {})
        self.capabilities = self.config.get('capabilities', [])
        
        # Log successful initialization
        logging.getLogger('dacp').info(
            f"🎯 Agent '{self.agent_metadata.get('name', 'unknown')}' initialized"
        )
    
    def setup_logging(self):
        """Configure DACP logging from embedded YAML configuration."""
        logging_config = AgentConfigLoader.extract_logging_config(self.config)
        
        if not logging_config.get('enabled', True):
            print("⚠️  Logging disabled in configuration")
            return
        
        # Apply logging configuration to DACP
        dacp_logging_args = {k: v for k, v in logging_config.items() if k != 'enabled'}
        dacp.setup_dacp_logging(**dacp_logging_args)
    
    def _load_intelligence_config(self) -> Dict[str, Any]:
        """Load intelligence configuration with environment variable support."""
        intelligence_config = self.config.get('intelligence', {}).copy()
        
        # Handle API keys from environment variables
        for key, value in intelligence_config.items():
            if key.endswith('_key') or key == 'api_key':
                # Auto-detect API key environment variables
                engine = intelligence_config.get('engine', '').upper()
                env_var = f"{engine}_API_KEY" if engine else 'API_KEY'
                intelligence_config[key] = os.getenv(env_var, value)
        
        return intelligence_config
    
    def handle_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Handle incoming messages based on YAML-defined capabilities."""
        task = message.get("task")
        
        # Generate capability handlers based on YAML capabilities
        {capability_handlers_generated_from_yaml}
        
        available_tasks = [cap['name'] for cap in self.capabilities]
        return {
            "error": f"Unknown task: {task}. Available tasks: {available_tasks}"
        }
```

### 4. Capability Handler Generation

For each capability in the YAML, generate handlers like this:

```python
# Generated based on capabilities in YAML
if task == "analyze_data":
    # Analyze datasets and generate insights
    try:
        result = dacp.invoke_intelligence(
            f"Analyze this data: {message.get('data', 'No data provided')}", 
            self.intelligence_config
        )
        return {"response": result}
    except Exception as e:
        return {"error": f"Analysis failed: {e}"}

elif task == "generate_report":
    # Generate analysis reports
    return {
        "tool_request": {
            "name": "file_writer",
            "args": {
                "path": f"./reports/{message.get('subject', 'report')}.txt",
                "content": f"Report: {message.get('subject', 'Generated Report')}\n"
            }
        }
    }

elif task == "custom_capability":
    # Handle custom capability
    return {"response": f"Executed {task} with data: {message}"}
```

### 5. Main Function Generation

Generate the main function with orchestrator setup:

```python
def main():
    """Run the generated agent with DACP logging."""
    # Create orchestrator and agent
    orchestrator = dacp.Orchestrator()
    agent = {AgentClassName}()
    agent_name = agent.agent_metadata.get('name', 'generated-agent')
    orchestrator.register_agent(agent_name, agent)
    
    print(f"🚀 Agent '{agent_name}' is running with DACP logging!")
    print("Available capabilities:")
    for capability in agent.capabilities:
        print(f"  • {capability['name']}: {capability.get('description', 'No description')}")
    
    # Example usage (optional)
    # You could generate example interactions here
    
    # Keep agent running or add your interaction loop
    print("Agent ready for messages...")

if __name__ == "__main__":
    main()
```

## Implementation Steps for OAS Generator

### Step 1: Update YAML Parser
- Add logging section parsing to your YAML schema validator
- Add the logging validation rules shown above
- Ensure backward compatibility (logging section is optional)

### Step 2: Update Code Templates
- Add DACP import statements to generated files
- Embed the `AgentConfigLoader` class in generated agents
- Modify agent base class to inherit from `dacp.Agent`
- Add `setup_logging()` call to agent constructor

### Step 3: Template Variables
Create these template variables from YAML parsing:

```python
# Variables to populate in templates
template_vars = {
    'agent_class_name': pascal_case(metadata['name']),
    'agent_name': metadata['name'],
    'logging_config': yaml_config['logging'],
    'intelligence_config': yaml_config['intelligence'],
    'capabilities': yaml_config['capabilities'],
    'metadata': yaml_config['metadata'],
    'capability_handlers': generate_capability_handlers(yaml_config['capabilities'])
}
```

### Step 4: Dependencies
Add DACP to generated requirements:

```txt
# In generated requirements.txt or setup.py
dacp>=0.3.0
```

## Expected Behavior After Implementation

### 1. Zero-Boilerplate Logging
```python
# User just runs generated agent
python3 my_generated_agent.py

# Gets automatic logging like:
# 2024-01-01 10:00:00 - 🚀 DACP logging configured: level=INFO, style=emoji
# 2024-01-01 10:00:01 - ✅ Agent 'my-agent' registered successfully
# 2024-01-01 10:00:02 - 📨 Sending message to agent 'my-agent'
# 2024-01-01 10:00:03 - 🧠 Invoking intelligence: engine='anthropic'
# 2024-01-01 10:00:04 - ✅ Intelligence call completed in 1.2s
```

### 2. Environment Variable Control
```bash
# Users can override logging without changing code
export DACP_LOG_LEVEL=DEBUG
export DACP_LOG_STYLE=detailed
export DACP_LOG_FILE=./debug.log

python3 my_generated_agent.py  # Uses environment overrides
```

### 3. Comprehensive Observability
Automatic logging for:
- Agent registration and lifecycle
- Message routing and timing
- LLM/intelligence provider calls with performance metrics
- Tool execution with arguments and results
- Error handling with full context
- Session management

## Testing Your Implementation

Create a test YAML file:

```yaml
apiVersion: "v1"
kind: "Agent"
metadata:
  name: "test-agent"
  type: "analysis"

logging:
  enabled: true
  level: "DEBUG"
  format_style: "emoji"
  log_file: "./logs/test.log"
  env_overrides:
    level: "DACP_LOG_LEVEL"

intelligence:
  engine: "anthropic"
  model: "claude-3-haiku-20240618"

capabilities:
  - name: "test_task"
    description: "Test capability"
```

Generate an agent from this YAML and verify:
1. Agent runs without errors
2. Logging appears in console and file
3. Environment variables override YAML settings
4. Agent responds to test messages
5. All DACP logging features work (intelligence calls, tool execution, etc.)

## Benefits for OAS Users

1. **Zero Configuration**: Logging works out of the box
2. **Production Ready**: Comprehensive observability for debugging and monitoring
3. **Flexible**: Environment variables allow runtime configuration changes
4. **Standardized**: All generated agents have consistent logging format
5. **Performance Monitoring**: Built-in timing and performance metrics
6. **Error Tracking**: Comprehensive error logging with context

This integration will significantly enhance the value proposition of OAS-generated agents by providing enterprise-grade logging and observability capabilities automatically. 