#!/usr/bin/env python3
"""
YAML Configuration Interface for DACP Logging

This example shows the complete code interface you need to implement
to load YAML configuration and properly integrate with DACP logging.
"""

import os
import yaml
import logging
from pathlib import Path
from typing import Dict, Any, Optional
import dacp


class AgentConfigLoader:
    """Handles loading and processing agent configuration from YAML files."""

    @staticmethod
    def load_config(config_path: str) -> Dict[str, Any]:
        """
        Load agent configuration from YAML file.

        Args:
            config_path: Path to YAML configuration file

        Returns:
            Parsed configuration dictionary

        Raises:
            FileNotFoundError: If config file doesn't exist
            yaml.YAMLError: If YAML is malformed
        """
        config_path = Path(config_path)
        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")

        try:
            with open(config_path, "r") as f:
                config = yaml.safe_load(f)
            return config or {}
        except yaml.YAMLError as e:
            raise yaml.YAMLError(f"Invalid YAML in {config_path}: {e}")

    @staticmethod
    def extract_logging_config(config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract and process logging configuration from agent config.

        Args:
            config: Full agent configuration dictionary

        Returns:
            Processed logging configuration ready for DACP
        """
        logging_config = config.get("logging", {})

        if not logging_config.get("enabled", True):
            return {"enabled": False}

        # Process environment variable overrides
        env_overrides = logging_config.get("env_overrides", {})
        processed_config = {}

        # Handle each logging parameter with env var fallback
        level = logging_config.get("level", "INFO")
        if "level" in env_overrides:
            level = os.getenv(env_overrides["level"], level)
        processed_config["level"] = level

        format_style = logging_config.get("format_style", "emoji")
        if "format_style" in env_overrides:
            format_style = os.getenv(env_overrides["format_style"], format_style)
        processed_config["format_style"] = format_style

        # Handle log file with directory creation
        log_file = logging_config.get("log_file")
        if "log_file" in env_overrides:
            log_file = os.getenv(env_overrides["log_file"], log_file)

        if log_file:
            # Ensure log directory exists
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)
            processed_config["log_file"] = str(log_path)

        # Other logging parameters
        processed_config["include_timestamp"] = logging_config.get(
            "include_timestamp", True
        )
        processed_config["enabled"] = True

        return processed_config


class ConfigurableAgent(dacp.Agent):
    """
    Base agent class that supports YAML configuration.

    This is the main interface you'd implement in your agent code.
    """

    def __init__(
        self, config_path: Optional[str] = None, config_dict: Optional[Dict] = None
    ):
        """
        Initialize agent with YAML configuration.

        Args:
            config_path: Path to YAML configuration file
            config_dict: Pre-loaded configuration dictionary (alternative to config_path)
        """
        # Load configuration
        if config_path:
            self.config = AgentConfigLoader.load_config(config_path)
        elif config_dict:
            self.config = config_dict
        else:
            self.config = {}

        # Setup logging first
        self.setup_logging()

        # Load other configurations
        self.intelligence_config = self._load_intelligence_config()
        self.agent_metadata = self.config.get("metadata", {})
        self.capabilities = self.config.get("capabilities", [])

        # Log successful initialization
        logging.getLogger("dacp").info(
            f"🎯 Agent '{self.agent_metadata.get('name', 'unknown')}' "
            f"initialized from {'YAML config' if config_path else 'config dict'}"
        )

    def setup_logging(self):
        """Configure DACP logging from YAML configuration."""
        logging_config = AgentConfigLoader.extract_logging_config(self.config)

        if not logging_config.get("enabled", True):
            print("⚠️  Logging disabled in configuration")
            return

        # Apply logging configuration to DACP
        dacp_logging_args = {k: v for k, v in logging_config.items() if k != "enabled"}
        dacp.setup_dacp_logging(**dacp_logging_args)

    def _load_intelligence_config(self) -> Dict[str, Any]:
        """Load intelligence configuration from YAML with environment variable support."""
        intelligence_config = self.config.get("intelligence", {}).copy()

        # Handle API keys from environment variables
        for key, value in intelligence_config.items():
            if (
                isinstance(value, str)
                and value.startswith("${")
                and value.endswith("}")
            ):
                # Handle ${ENV_VAR} syntax
                env_var = value[2:-1]
                intelligence_config[key] = os.getenv(env_var)
            elif key.endswith("_key") or key == "api_key":
                # Auto-detect API key environment variables
                env_var = key.upper()
                if env_var not in os.environ:
                    # Try common patterns
                    engine = intelligence_config.get("engine", "").upper()
                    if engine:
                        env_var = f"{engine}_API_KEY"

                intelligence_config[key] = os.getenv(env_var, value)

        return intelligence_config

    def handle_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle incoming messages based on YAML-defined capabilities.

        Override this method in your specific agent implementation.
        """
        task = message.get("task")

        # Find matching capability
        for capability in self.capabilities:
            if capability["name"] == task:
                return self._handle_capability(capability, message)

        available_tasks = [cap["name"] for cap in self.capabilities]
        return {"error": f"Unknown task: {task}. Available tasks: {available_tasks}"}

    def _handle_capability(
        self, capability: Dict[str, Any], message: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Handle a specific capability. Override this for custom behavior.

        Args:
            capability: Capability definition from YAML
            message: Incoming message

        Returns:
            Response dictionary
        """
        # Default implementation - override in subclasses
        return {
            "response": f"Executed capability '{capability['name']}' with message: {message}"
        }


class SmartAnalysisAgent(ConfigurableAgent):
    """
    Example implementation of a configurable agent with specific capabilities.

    This shows how you'd extend the base ConfigurableAgent for your use case.
    """

    def _handle_capability(
        self, capability: Dict[str, Any], message: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Handle capabilities with specific business logic."""
        capability_name = capability["name"]

        if capability_name == "analyze_data":
            return self._analyze_data(message)
        elif capability_name == "generate_report":
            return self._generate_report(message)
        elif capability_name == "visualize_data":
            return self._visualize_data(message)
        else:
            # Fallback to parent implementation
            return super()._handle_capability(capability, message)

    def _analyze_data(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze data using configured intelligence provider."""
        data = message.get("data", "No data provided")

        try:
            result = dacp.invoke_intelligence(
                f"Analyze this data and provide insights: {data}",
                self.intelligence_config,
            )
            return {"response": result}
        except Exception as e:
            return {"error": f"Analysis failed: {e}"}

    def _generate_report(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a report using the file_writer tool."""
        subject = message.get("subject", "report")
        content = f"Analysis Report: {subject}\n\nGenerated from data: {message.get('data', 'N/A')}\n"

        return {
            "tool_request": {
                "name": "file_writer",
                "args": {
                    "path": f"./reports/{subject.replace(' ', '_')}.txt",
                    "content": content,
                },
            }
        }

    def _visualize_data(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Create data visualization (mock implementation)."""
        return {
            "response": f"Created visualization for: {message.get('data', 'unknown data')}"
        }


def create_agent_from_yaml(config_path: str) -> ConfigurableAgent:
    """
    Factory function to create an agent from YAML configuration.

    This is the main interface you'd expose to users.

    Args:
        config_path: Path to YAML configuration file

    Returns:
        Configured agent instance
    """
    try:
        config = AgentConfigLoader.load_config(config_path)
        agent_type = config.get("metadata", {}).get("type", "smart_analysis")

        # Create appropriate agent type based on config
        if agent_type == "smart_analysis":
            return SmartAnalysisAgent(config_dict=config)
        else:
            # Default to base configurable agent
            return ConfigurableAgent(config_dict=config)

    except Exception as e:
        print(f"❌ Failed to create agent from {config_path}: {e}")
        raise


def main():
    """Demo the YAML configuration interface."""
    print("🔧 YAML Configuration Interface Demo\n")

    # Test 1: Direct YAML loading
    print("=" * 60)
    print("📋 Test 1: Loading Agent from YAML Configuration")
    print("=" * 60)

    try:
        agent = create_agent_from_yaml("examples/oas_agent_config.yaml")

        # Create orchestrator and register agent
        orchestrator = dacp.Orchestrator()
        agent_name = agent.agent_metadata.get("name", "configured-agent")
        orchestrator.register_agent(agent_name, agent)

        print(f"✅ Agent '{agent_name}' created and registered successfully")
        print(f"📊 Capabilities: {[cap['name'] for cap in agent.capabilities]}")
        print(f"🧠 Intelligence: {agent.intelligence_config.get('engine', 'unknown')}")

        # Test messaging
        test_messages = [
            {"task": "analyze_data", "data": "sample dataset with user interactions"},
            {
                "task": "generate_report",
                "subject": "User Behavior Analysis",
                "data": "user metrics",
            },
            {"task": "visualize_data", "data": "user engagement trends"},
        ]

        for msg in test_messages:
            print(f"\n📨 Sending: {msg}")
            response = orchestrator.send_message(agent_name, msg)
            print(f"📤 Response: {response}")

    except Exception as e:
        print(f"❌ Demo failed: {e}")

    # Test 2: Configuration validation
    print(f"\n{'='*60}")
    print("📋 Test 2: Configuration Validation")
    print("=" * 60)

    # Show what the configuration looks like after processing
    try:
        config = AgentConfigLoader.load_config("examples/oas_agent_config.yaml")
        logging_config = AgentConfigLoader.extract_logging_config(config)

        print("✅ Configuration loaded successfully:")
        print(f"  📝 Agent: {config.get('metadata', {}).get('name', 'unknown')}")
        print(f"  📊 Logging Level: {logging_config.get('level', 'unknown')}")
        print(f"  🎨 Format Style: {logging_config.get('format_style', 'unknown')}")
        print(f"  📁 Log File: {logging_config.get('log_file', 'console only')}")
        print(
            f"  ⚙️  Intelligence Engine: {config.get('intelligence', {}).get('engine', 'unknown')}"
        )

    except Exception as e:
        print(f"❌ Configuration validation failed: {e}")

    print("\n" + "=" * 60)
    print("💡 Interface Summary")
    print("=" * 60)
    print("1. Use AgentConfigLoader.load_config() to load YAML")
    print("2. Use AgentConfigLoader.extract_logging_config() to process logging")
    print("3. Extend ConfigurableAgent for your specific agent implementation")
    print("4. Use create_agent_from_yaml() as your main factory function")
    print("5. DACP logging is automatically configured from YAML")


if __name__ == "__main__":
    main()
