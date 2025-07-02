#!/usr/bin/env python3
"""
DACP Logging Demo

This script demonstrates how to use DACP's logging capabilities to track
agent operations, tool executions, and intelligence calls.
"""

import dacp
import time


class LoggingDemoAgent(dacp.Agent):
    """A demo agent that showcases various DACP operations."""
    
    def handle_message(self, message):
        task = message.get("task")
        
        if task == "greet":
            return {
                "response": f"Hello, {message.get('name', 'World')}! 👋"
            }
        
        elif task == "write_file":
            # Request the file_writer tool
            return {
                "tool_request": {
                    "name": "file_writer",
                    "args": {
                        "path": "./output/demo_file.txt",
                        "content": f"Demo file created at {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
                    }
                }
            }
        
        elif task == "intelligence":
            # Simulate using the intelligence function
            # (This would normally be called by the agent internally)
            return {
                "response": "I would call invoke_intelligence here with a config, but no API keys are set for this demo."
            }
        
        elif task == "error":
            # Demonstrate error handling
            raise Exception("This is a demo error to show logging")
        
        else:
            return {
                "error": f"Unknown task: {task}. Available tasks: greet, write_file, intelligence, error"
            }


def demo_basic_logging():
    """Demo basic logging with emoji format."""
    print("=" * 60)
    print("🎯 Demo 1: Basic Logging (INFO level, emoji format)")
    print("=" * 60)
    
    # Enable basic logging
    dacp.enable_info_logging()
    
    # Create orchestrator and agent
    orchestrator = dacp.Orchestrator()
    agent = LoggingDemoAgent()
    orchestrator.register_agent("demo-agent", agent)
    
    # Send some messages
    print("\n📤 Sending greeting message...")
    response = orchestrator.send_message("demo-agent", {
        "task": "greet",
        "name": "Alice"
    })
    print(f"Response: {response}")
    
    print("\n📤 Sending file write request...")
    response = orchestrator.send_message("demo-agent", {
        "task": "write_file"
    })
    print(f"Response: {response}")
    
    print("\n📊 Session info:")
    print(orchestrator.get_session_info())


def demo_debug_logging():
    """Demo detailed logging with DEBUG level."""
    print("\n" + "=" * 60)
    print("🔍 Demo 2: Debug Logging (DEBUG level, detailed format)")
    print("=" * 60)
    
    # Enable debug logging
    dacp.enable_debug_logging()
    
    # Create orchestrator and agent
    orchestrator = dacp.Orchestrator()
    agent = LoggingDemoAgent()
    orchestrator.register_agent("debug-agent", agent)
    
    # Send a message that will trigger tool execution
    print("\n📤 Sending file write request with debug logging...")
    response = orchestrator.send_message("debug-agent", {
        "task": "write_file"
    })
    print(f"Response: {response}")


def demo_error_logging():
    """Demo error logging."""
    print("\n" + "=" * 60)
    print("❌ Demo 3: Error Logging")
    print("=" * 60)
    
    # Create orchestrator and agent
    orchestrator = dacp.Orchestrator()
    agent = LoggingDemoAgent()
    orchestrator.register_agent("error-agent", agent)
    
    # Send a message that will cause an error
    print("\n📤 Sending message that will cause an error...")
    response = orchestrator.send_message("error-agent", {
        "task": "error"
    })
    print(f"Response: {response}")
    
    # Try to send message to non-existent agent
    print("\n📤 Sending message to non-existent agent...")
    response = orchestrator.send_message("non-existent", {
        "task": "anything"
    })
    print(f"Response: {response}")


def demo_intelligence_logging():
    """Demo intelligence provider logging."""
    print("\n" + "=" * 60)
    print("🧠 Demo 4: Intelligence Provider Logging")
    print("=" * 60)
    
    # Test intelligence with invalid config (will show error logs)
    print("\n🧠 Testing intelligence with missing engine...")
    try:
        dacp.invoke_intelligence("Hello", {})
    except Exception as e:
        print(f"Expected error: {e}")
    
    print("\n🧠 Testing intelligence with unsupported engine...")
    try:
        dacp.invoke_intelligence("Hello", {"engine": "unsupported"})
    except Exception as e:
        print(f"Expected error: {e}")
    
    print("\n🧠 Testing intelligence with missing API key...")
    try:
        dacp.invoke_intelligence("Hello", {
            "engine": "openai",
            "model": "gpt-4"
        })
    except Exception as e:
        print(f"Expected error: {e}")


def demo_broadcast_logging():
    """Demo broadcast logging."""
    print("\n" + "=" * 60)
    print("📡 Demo 5: Broadcast Logging")
    print("=" * 60)
    
    # Create orchestrator with multiple agents
    orchestrator = dacp.Orchestrator()
    
    agent1 = LoggingDemoAgent()
    agent2 = LoggingDemoAgent()
    agent3 = LoggingDemoAgent()
    
    orchestrator.register_agent("agent-1", agent1)
    orchestrator.register_agent("agent-2", agent2)
    orchestrator.register_agent("agent-3", agent3)
    
    # Broadcast a message
    print("\n📡 Broadcasting greeting to all agents...")
    responses = orchestrator.broadcast_message({
        "task": "greet",
        "name": "Everyone"
    })
    
    for agent_id, response in responses.items():
        print(f"  {agent_id}: {response}")


def main():
    """Run all logging demos."""
    print("🚀 DACP Logging Demonstration")
    print("This demo shows DACP's logging capabilities across different operations.\n")
    
    # Run demos
    demo_basic_logging()
    demo_debug_logging()
    demo_error_logging()
    demo_intelligence_logging()
    demo_broadcast_logging()
    
    print("\n" + "=" * 60)
    print("✅ Demo Complete!")
    print("=" * 60)
    print("\n💡 Logging Tips:")
    print("• Use dacp.enable_info_logging() for production monitoring")
    print("• Use dacp.enable_debug_logging() for development and troubleshooting")
    print("• Use dacp.enable_quiet_logging() to only see errors")
    print("• Use dacp.setup_dacp_logging() for custom configuration")
    print("• Add log_file parameter to save logs to a file")
    print("\nExample configuration:")
    print("  dacp.setup_dacp_logging(level='INFO', format_style='emoji', log_file='dacp.log')")


if __name__ == "__main__":
    main() 