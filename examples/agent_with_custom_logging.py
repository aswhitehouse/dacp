#!/usr/bin/env python3
"""
Agent with Custom Logging Configuration

This example shows how to integrate DACP logging configuration directly 
into your agent code, including loading config from environment variables
or configuration files.
"""

import os
import yaml
import dacp


class MyAgent(dacp.Agent):
    """An agent with built-in logging configuration."""

    def __init__(self, log_config=None):
        """Initialize agent with optional logging configuration."""
        self.setup_logging(log_config)

    def setup_logging(self, log_config=None):
        """Configure DACP logging based on provided config or environment."""
        if log_config:
            # Use provided configuration
            dacp.setup_dacp_logging(**log_config)
        else:
            # Check environment variables for logging config
            log_level = os.getenv("DACP_LOG_LEVEL", "INFO")
            log_style = os.getenv("DACP_LOG_STYLE", "emoji")
            log_file = os.getenv("DACP_LOG_FILE")

            dacp.setup_dacp_logging(
                level=log_level,
                format_style=log_style,
                include_timestamp=True,
                log_file=log_file,
            )

    def handle_message(self, message):
        """Handle incoming messages."""
        task = message.get("task")

        if task == "greet":
            return {"response": f"Hello, {message.get('name', 'World')}!"}

        elif task == "analyze":
            # Use intelligence with logging
            intelligence_config = {
                "engine": "anthropic",
                "model": "claude-3-haiku-20240307",
                "api_key": os.getenv("ANTHROPIC_API_KEY"),
            }

            try:
                if intelligence_config["api_key"]:
                    result = dacp.invoke_intelligence(
                        f"Analyze this data: {message.get('data', 'No data provided')}",
                        intelligence_config,
                    )
                    return {"response": result}
                else:
                    return {"response": "No API key configured for intelligence"}
            except Exception as e:
                return {"error": f"Intelligence analysis failed: {e}"}

        elif task == "write_report":
            # Use tools with logging
            return {
                "tool_request": {
                    "name": "file_writer",
                    "args": {
                        "path": "./reports/analysis_report.txt",
                        "content": f"Report generated for: {message.get('subject', 'Unknown')}\n",
                    },
                }
            }

        else:
            return {"error": f"Unknown task: {task}"}


def load_config_from_yaml(config_file):
    """Load configuration from YAML file."""
    try:
        with open(config_file, "r") as f:
            config = yaml.safe_load(f)
        return config.get("logging", {})
    except FileNotFoundError:
        print(f"Config file {config_file} not found, using defaults")
        return {}
    except Exception as e:
        print(f"Error loading config: {e}")
        return {}


def main():
    """Run agent with different logging configurations."""
    print("🚀 Agent with Custom Logging Demo\n")

    # Example 1: Environment-based configuration
    print("=" * 60)
    print("📋 Example 1: Environment-based Configuration")
    print("=" * 60)

    # Set some example environment variables
    os.environ["DACP_LOG_LEVEL"] = "DEBUG"
    os.environ["DACP_LOG_STYLE"] = "detailed"

    agent1 = MyAgent()
    orchestrator1 = dacp.Orchestrator()
    orchestrator1.register_agent("env-agent", agent1)

    response = orchestrator1.send_message(
        "env-agent", {"task": "greet", "name": "Environment User"}
    )
    print(f"Response: {response}")

    # Example 2: Direct configuration
    print("\n" + "=" * 60)
    print("📋 Example 2: Direct Configuration")
    print("=" * 60)

    log_config = {
        "level": "INFO",
        "format_style": "emoji",
        "include_timestamp": False,
        "log_file": "agent.log",
    }

    agent2 = MyAgent(log_config)
    orchestrator2 = dacp.Orchestrator()
    orchestrator2.register_agent("direct-agent", agent2)

    response = orchestrator2.send_message(
        "direct-agent", {"task": "write_report", "subject": "Custom Logging Test"}
    )
    print(f"Response: {response}")

    # Example 3: YAML configuration
    print("\n" + "=" * 60)
    print("📋 Example 3: YAML Configuration")
    print("=" * 60)

    # Create a sample config file
    sample_config = {
        "logging": {
            "level": "WARNING",
            "format_style": "simple",
            "include_timestamp": True,
        }
    }

    with open("agent_config.yaml", "w") as f:
        yaml.dump(sample_config, f)

    yaml_log_config = load_config_from_yaml("agent_config.yaml")
    agent3 = MyAgent(yaml_log_config)
    orchestrator3 = dacp.Orchestrator()
    orchestrator3.register_agent("yaml-agent", agent3)

    response = orchestrator3.send_message(
        "yaml-agent", {"task": "greet", "name": "YAML User"}
    )
    print(f"Response: {response}")

    print("\n" + "=" * 60)
    print("✅ Demo Complete!")
    print("=" * 60)

    print("\n💡 Integration Options:")
    print("1. Environment Variables:")
    print("   export DACP_LOG_LEVEL=DEBUG")
    print("   export DACP_LOG_STYLE=emoji")
    print("   export DACP_LOG_FILE=agent.log")
    print("\n2. Configuration File (YAML/JSON):")
    print("   logging:")
    print("     level: INFO")
    print("     format_style: emoji")
    print("     log_file: ./logs/agent.log")
    print("\n3. Direct Configuration:")
    print("   agent = MyAgent({")
    print("       'level': 'DEBUG',")
    print("       'format_style': 'detailed'")
    print("   })")


if __name__ == "__main__":
    main()
