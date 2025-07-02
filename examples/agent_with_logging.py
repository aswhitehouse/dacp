#!/usr/bin/env python3
"""
Simple Agent with DACP Logging Example

This demonstrates the basic pattern for using DACP agents with logging enabled.
"""

import dacp


class SimpleAgent(dacp.Agent):
    """A simple agent that demonstrates common operations."""
    
    def handle_message(self, message):
        task = message.get("task")
        
        if task == "greet":
            name = message.get("name", "World")
            return {"response": f"Hello, {name}!"}
        
        elif task == "write_note":
            content = message.get("content", "Default note content")
            return {
                "tool_request": {
                    "name": "file_writer",
                    "args": {
                        "path": "./notes/note.txt",
                        "content": content
                    }
                }
            }
        
        elif task == "use_intelligence":
            # In a real agent, you'd call invoke_intelligence here
            # For this demo, we'll just simulate it
            intelligence_config = {
                "engine": "anthropic",
                "model": "claude-3-haiku-20240307"
                # API key would come from environment or config
            }
            
            try:
                # This would normally work with proper API key
                # result = dacp.invoke_intelligence("Hello AI", intelligence_config)
                return {"response": "Would call invoke_intelligence here (no API key set for demo)"}
            except Exception as e:
                return {"error": f"Intelligence call failed: {e}"}
        
        else:
            return {"error": f"Unknown task: {task}"}


def main():
    """Run the agent example with logging."""
    print("🚀 DACP Agent with Logging Example\n")
    
    # Enable logging (try different levels/styles)
    print("Enabling DACP logging...")
    dacp.enable_info_logging()
    
    # Create orchestrator and agent
    orchestrator = dacp.Orchestrator()
    agent = SimpleAgent()
    orchestrator.register_agent("simple-agent", agent)
    
    print("\n" + "="*50)
    print("📤 Sending greeting message...")
    response = orchestrator.send_message("simple-agent", {
        "task": "greet",
        "name": "Alice"
    })
    print(f"Response: {response}")
    
    print("\n" + "="*50)
    print("📤 Requesting file write...")
    response = orchestrator.send_message("simple-agent", {
        "task": "write_note",
        "content": "This is a note written by an agent!"
    })
    print(f"Response: {response}")
    
    print("\n" + "="*50)
    print("📤 Requesting intelligence call...")
    response = orchestrator.send_message("simple-agent", {
        "task": "use_intelligence"
    })
    print(f"Response: {response}")
    
    print("\n" + "="*50)
    print("📊 Session Information:")
    session_info = orchestrator.get_session_info()
    for key, value in session_info.items():
        print(f"  {key}: {value}")
    
    print("\n✅ Example complete!")
    print("\n💡 Try running with different logging levels:")
    print("   dacp.enable_debug_logging()  # See detailed debug info")
    print("   dacp.enable_quiet_logging()  # Only errors")


if __name__ == "__main__":
    main() 