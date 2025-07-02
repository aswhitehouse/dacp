# DACP Logging Integration for Open Agent Spec (OAS)

## Goal
Integrate DACP's comprehensive logging system into OAS so generated agents automatically have enterprise-grade observability with zero boilerplate code.

## Required YAML Schema Addition

Add this new `logging` section to your OAS YAML specification:

```yaml
# New logging section to add to OAS schema
logging:
  enabled: true                    # Whether to enable DACP logging  
  level: "INFO"                    # DEBUG, INFO, WARNING, ERROR, CRITICAL
  format_style: "emoji"            # emoji, detailed, simple
  include_timestamp: true          # Include timestamps in logs
  log_file: "./logs/agent.log"     # Optional: log to file (auto-creates dirs)
  
  # Environment variable overrides (runtime configuration)
  env_overrides:
    level: "DACP_LOG_LEVEL"        # env var that overrides level
    format_style: "DACP_LOG_STYLE" # env var that overrides format_style  
    log_file: "DACP_LOG_FILE"      # env var that overrides log_file
```

## Required Code Generation Changes

### 1. Add DACP Import
```python
import dacp
```

### 2. Change Agent Base Class
```python
# Instead of your current base class:
class {AgentName}(dacp.Agent):  # Inherit from dacp.Agent
```

### 3. Add Logging Setup in Constructor
```python
def __init__(self):
    # Embed YAML config as dict during generation
    self.config = {
        "logging": {logging_section_from_yaml},
        "intelligence": {intelligence_section_from_yaml},
        # ... other sections
    }
    
    # Setup DACP logging FIRST
    self.setup_logging()
    
    # Continue with existing initialization...

def setup_logging(self):
    """Configure DACP logging from YAML configuration."""
    logging_config = self.config.get('logging', {})
    
    if not logging_config.get('enabled', True):
        return
    
    # Process environment variable overrides
    env_overrides = logging_config.get('env_overrides', {})
    
    level = logging_config.get('level', 'INFO')
    if 'level' in env_overrides:
        level = os.getenv(env_overrides['level'], level)
    
    format_style = logging_config.get('format_style', 'emoji')
    if 'format_style' in env_overrides:
        format_style = os.getenv(env_overrides['format_style'], format_style)
    
    log_file = logging_config.get('log_file')
    if 'log_file' in env_overrides:
        log_file = os.getenv(env_overrides['log_file'], log_file)
    
    # Create log directory if needed
    if log_file:
        Path(log_file).parent.mkdir(parents=True, exist_ok=True)
    
    # Configure DACP logging
    dacp.setup_dacp_logging(
        level=level,
        format_style=format_style,
        include_timestamp=logging_config.get('include_timestamp', True),
        log_file=log_file
    )
```

### 4. Add DACP Dependency
```txt
# Add to generated requirements.txt
dacp>=0.3.0
```

## What Users Get Automatically

### Zero-Config Logging
```bash
python3 generated_agent.py

# Automatic output:
# 2024-01-01 10:00:00 - 🚀 DACP logging configured: level=INFO, style=emoji
# 2024-01-01 10:00:01 - ✅ Agent 'my-agent' registered successfully  
# 2024-01-01 10:00:02 - 📨 Sending message to agent 'my-agent'
# 2024-01-01 10:00:03 - 🧠 Invoking intelligence: engine='anthropic', model='claude-3-haiku'
# 2024-01-01 10:00:04 - ✅ Intelligence call completed in 1.2s
# 2024-01-01 10:00:05 - 🛠️  Executing tool: 'file_writer' with args: {...}
# 2024-01-01 10:00:06 - ✅ Tool executed successfully in 0.1s
```

### Runtime Configuration
```bash
# Users can override logging without code changes
export DACP_LOG_LEVEL=DEBUG
export DACP_LOG_STYLE=detailed  
export DACP_LOG_FILE=./debug.log

python3 generated_agent.py  # Uses environment overrides
```

## Comprehensive Observability Coverage

DACP automatically logs:
- 🎭 Agent registration and lifecycle events
- 📨 Message routing with timing and content (debug level)
- 🧠 LLM calls with provider, model, performance metrics
- 🛠️ Tool execution with arguments, results, and timing
- ❌ Error handling with full context and stack traces  
- 💾 Session management and conversation history
- 🔧 Orchestrator operations and agent interactions

## Implementation Benefits

1. **Zero Boilerplate**: No logging code needed in generated agents
2. **Production Ready**: Enterprise-grade observability out of the box
3. **Runtime Flexible**: Environment variables override YAML settings
4. **Performance Monitoring**: Built-in timing and metrics
5. **Debugging Power**: Comprehensive error tracking with context
6. **Standardized**: All OAS agents have consistent logging format

## Quick Test

Generate an agent with this YAML:

```yaml
apiVersion: "v1"
kind: "Agent" 
metadata:
  name: "test-agent"

logging:
  enabled: true
  level: "DEBUG"
  format_style: "emoji"

intelligence:
  engine: "anthropic"
  model: "claude-3-haiku-20240618"

capabilities:
  - name: "test_task"
```

The generated agent should run with comprehensive logging automatically enabled.

## Key Integration Points

1. **YAML Parser**: Add logging section to schema validation
2. **Code Templates**: Modify agent constructor to call `setup_logging()`
3. **Base Class**: Change from your current base to `dacp.Agent`
4. **Dependencies**: Add `dacp>=0.3.0` to generated requirements
5. **Config Embedding**: Embed YAML config as dict in generated Python

This integration provides massive value-add for OAS users with minimal implementation effort. 