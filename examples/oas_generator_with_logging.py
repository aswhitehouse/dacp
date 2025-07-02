#!/usr/bin/env python3
"""
OAS Generator with DACP Logging Integration

This example shows how an Open Agent Spec generator could automatically
integrate DACP logging configuration into generated agent code.
"""

import yaml
import dacp
from typing import Dict, Any


def generate_agent_from_oas(config_file: str) -> str:
    """
    Generate agent code from OAS YAML configuration with DACP logging.

    Args:
        config_file: Path to OAS YAML configuration file

    Returns:
        Generated Python agent code as string
    """

    # Load OAS configuration
    with open(config_file, "r") as f:
        config = yaml.safe_load(f)

    # Extract configuration sections
    metadata = config.get("metadata", {})
    intelligence_config = config.get("intelligence", {})
    logging_config = config.get("logging", {})
    capabilities = config.get("capabilities", [])

    # Generate agent code
    agent_code = f'''#!/usr/bin/env python3
"""
{metadata.get('description', 'Generated agent')}

Generated from OAS configuration: {config_file}
Agent: {metadata.get('name', 'unknown')}
Version: {metadata.get('version', '1.0.0')}
"""

import os
import dacp


class {_to_class_name(metadata.get('name', 'GeneratedAgent'))}(dacp.Agent):
    """Generated agent class from OAS specification."""
    
    def __init__(self):
        """Initialize agent with OAS configuration."""
        self.setup_logging()
        self.intelligence_config = self._load_intelligence_config()
        
    def setup_logging(self):
        """Configure DACP logging from OAS specification."""
        {_generate_logging_setup(logging_config)}
        
    def _load_intelligence_config(self):
        """Load intelligence configuration from OAS spec."""
        return {_generate_intelligence_config(intelligence_config)}
        
    def handle_message(self, message):
        """Handle incoming messages based on OAS capabilities."""
        task = message.get("task")
        
        {_generate_capability_handlers(capabilities)}
        
        return {{"error": f"Unknown task: {{task}}. Available tasks: {[cap['name'] for cap in capabilities]}"}}


def main():
    """Run the generated agent."""
    # Create orchestrator and agent
    orchestrator = dacp.Orchestrator()
    agent = {_to_class_name(metadata.get('name', 'GeneratedAgent'))}()
    orchestrator.register_agent("{metadata.get('name', 'agent')}", agent)
    
    print("🚀 Generated agent is running with DACP logging!")
    print("Available capabilities:")
    {_generate_capability_list(capabilities)}
    
    # Example usage
    test_messages = [
        {{"task": "analyze_data", "data": "sample dataset"}},
        {{"task": "generate_report", "subject": "Test Analysis"}},
    ]
    
    for msg in test_messages:
        print(f"\\nSending: {{msg}}")
        response = orchestrator.send_message("{metadata.get('name', 'agent')}", msg)
        print(f"Response: {{response}}")


if __name__ == "__main__":
    main()
'''

    return agent_code


def _to_class_name(name: str) -> str:
    """Convert agent name to valid Python class name."""
    # Remove non-alphanumeric characters and convert to PascalCase
    clean_name = "".join(
        word.capitalize()
        for word in name.replace("-", "_").replace(" ", "_").split("_")
        if word.isalnum()
    )
    return clean_name + "Agent" if not clean_name.endswith("Agent") else clean_name


def _generate_logging_setup(logging_config: Dict[str, Any]) -> str:
    """Generate logging setup code from OAS logging configuration."""
    if not logging_config.get("enabled", True):
        return "        # Logging disabled in OAS configuration"

    level = logging_config.get("level", "INFO")
    format_style = logging_config.get("format_style", "emoji")
    include_timestamp = logging_config.get("include_timestamp", True)
    log_file = logging_config.get("log_file")
    env_overrides = logging_config.get("env_overrides", {})

    setup_lines = []

    # Environment variable overrides
    if env_overrides:
        if "level" in env_overrides:
            setup_lines.append(
                f'        level = os.getenv("{env_overrides["level"]}", "{level}")'
            )
        if "format_style" in env_overrides:
            setup_lines.append(
                f'        format_style = os.getenv("{env_overrides["format_style"]}", "{format_style}")'
            )
        if "log_file" in env_overrides:
            setup_lines.append(
                f'        log_file = os.getenv("{env_overrides["log_file"]}", {repr(log_file)})'
            )

    if not setup_lines:
        # Direct configuration
        setup_lines = [
            f'        level = "{level}"',
            f'        format_style = "{format_style}"',
            f"        log_file = {repr(log_file)}",
        ]

    setup_lines.append(
        f"""        
        dacp.setup_dacp_logging(
            level=level,
            format_style=format_style,
            include_timestamp={include_timestamp},
            log_file=log_file
        )"""
    )

    return "\n".join(setup_lines)


def _generate_intelligence_config(intelligence_config: Dict[str, Any]) -> str:
    """Generate intelligence configuration from OAS spec."""
    config_lines = ["{"]

    for key, value in intelligence_config.items():
        if key.endswith("_key") or key == "api_key":
            # Load from environment variable
            env_var = key.upper()
            config_lines.append(f'            "{key}": os.getenv("{env_var}"),')
        else:
            config_lines.append(f'            "{key}": {repr(value)},')

    config_lines.append("        }")
    return "\n".join(config_lines)


def _generate_capability_handlers(capabilities: list) -> str:
    """Generate message handlers for each capability."""
    handlers = []

    for capability in capabilities:
        name = capability["name"]
        description = capability.get("description", f"Handle {name} task")

        if name == "analyze_data":
            handler = f"""if task == "{name}":
            # {description}
            try:
                result = dacp.invoke_intelligence(
                    f"Analyze this data: {{message.get('data', 'No data provided')}}", 
                    self.intelligence_config
                )
                return {{"response": result}}
            except Exception as e:
                return {{"error": f"Analysis failed: {{e}}"}}"""

        elif name == "generate_report":
            handler = f"""if task == "{name}":
            # {description}
            return {{
                "tool_request": {{
                    "name": "file_writer",
                    "args": {{
                        "path": "./reports/{{message.get('subject', 'report')}}.txt",
                        "content": f"Report: {{message.get('subject', 'Generated Report')}}\\n"
                    }}
                }}
            }}"""

        else:
            # Generic handler
            handler = f"""if task == "{name}":
            # {description}
            return {{"response": f"Executed {name} with data: {{message}}"}}"""

        handlers.append("        " + handler.replace("\n", "\n        "))

    return "\n        \nel".join(handlers)


def _generate_capability_list(capabilities: list) -> str:
    """Generate code to print capability list."""
    lines = []
    for capability in capabilities:
        name = capability["name"]
        description = capability.get("description", "No description")
        lines.append(f'    print("  • {name}: {description}")')
    return "\n".join(lines)


def main():
    """Demo the OAS generator with logging integration."""
    print("🔧 OAS Generator with DACP Logging Integration Demo\\n")

    # Generate agent code from OAS configuration
    print("Generating agent from OAS configuration...")
    agent_code = generate_agent_from_oas("examples/oas_agent_config.yaml")

    # Save generated code
    output_file = "generated_agent.py"
    with open(output_file, "w") as f:
        f.write(agent_code)

    print(f"✅ Generated agent code saved to: {output_file}")
    print("\\n📋 Generated code preview:")
    print("-" * 50)
    print(agent_code[:1000] + "..." if len(agent_code) > 1000 else agent_code)
    print("-" * 50)

    print("\\n💡 The generated agent includes:")
    print("  • Automatic DACP logging configuration from OAS spec")
    print("  • Intelligence configuration with environment variable support")
    print("  • Capability-based message handlers")
    print("  • Built-in error handling and logging")

    print(f"\\n🚀 To run the generated agent:")
    print(f"   python3 {output_file}")


if __name__ == "__main__":
    main()
