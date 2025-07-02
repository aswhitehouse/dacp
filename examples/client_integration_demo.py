#!/usr/bin/env python3
"""
DACP Client Integration Demo

This demonstrates how a client user can independently use DACP as their
agent router for tools, LLMs, and multi-agent workflows without any
additional setup or dependencies beyond pip install dacp.
"""

import dacp
import os


class ClientAgent(dacp.Agent):
    """
    Example of a client's custom agent using DACP as the router.

    This shows the minimal interface needed for any client to create
    agents that work with DACP's routing, tools, and LLM capabilities.
    """

    def handle_message(self, message):
        """Handle various client tasks using DACP's routing capabilities."""
        task = message.get("task")

        if task == "analyze_with_ai":
            # Client wants to use LLM analysis
            data = message.get("data", "No data provided")

            # Use DACP's intelligence routing
            intelligence_config = {
                "engine": "anthropic",  # or "openai", "azure", "local"
                "model": "claude-3-haiku-20240307",
                # API key from environment: ANTHROPIC_API_KEY
            }

            try:
                result = dacp.invoke_intelligence(
                    f"Please analyze this data and provide insights: {data}",
                    intelligence_config,
                )
                return {"response": result}
            except Exception as e:
                return {"error": f"AI analysis failed: {e}"}

        elif task == "create_report":
            # Client wants to generate files using DACP's tools
            subject = message.get("subject", "Report")
            content = message.get("content", "No content provided")

            return {
                "tool_request": {
                    "name": "file_writer",
                    "args": {
                        "path": f"./client_reports/{subject.replace(' ', '_')}.txt",
                        "content": f"# {subject}\n\n{content}\n\nGenerated via DACP routing\n",
                    },
                }
            }

        elif task == "process_workflow":
            # Client wants multi-step workflow
            return self._handle_client_workflow(message)

        elif task == "custom_tool":
            # Client can use any registered tool through DACP
            tool_name = message.get("tool_name", "file_writer")
            tool_args = message.get("tool_args", {})

            return {"tool_request": {"name": tool_name, "args": tool_args}}

        else:
            return {
                "error": f"Unknown task: {task}",
                "available_tasks": [
                    "analyze_with_ai",
                    "create_report",
                    "process_workflow",
                    "custom_tool",
                ],
            }

    def _handle_client_workflow(self, message):
        """Example of client's custom multi-step workflow."""
        workflow_type = message.get("workflow_type", "simple")

        if workflow_type == "analysis_report":
            # Step 1: Analyze data with AI
            data = message.get("data", "Sample data")

            # This would normally be a multi-step process, but for demo
            # we'll show how DACP routes both AI and tool requests
            return {
                "workflow_status": "step_1_ai_analysis",
                "intelligence_request": {
                    "engine": "anthropic",
                    "model": "claude-3-haiku-20240307",
                    "prompt": f"Analyze: {data}",
                },
                "response": "Starting analysis workflow with DACP routing",
            }

        return {"response": "Workflow type not implemented"}


def demo_independent_client_usage():
    """
    Show how a client can independently use DACP as their agent router.

    This demonstrates the complete interface available to clients.
    """
    print("🚀 DACP Independent Client Usage Demo")
    print("=" * 60)

    # Step 1: Enable logging (optional but recommended)
    print("\n1️⃣  Setting up DACP logging...")
    dacp.enable_info_logging()

    # Step 2: Create orchestrator (DACP's agent router)
    print("\n2️⃣  Creating DACP orchestrator (agent router)...")
    orchestrator = dacp.Orchestrator()

    # Step 3: Register client's custom agent
    print("\n3️⃣  Registering client agent with DACP router...")
    client_agent = ClientAgent()
    orchestrator.register_agent("client-agent", client_agent)

    print("\n✅ DACP is now routing for client agent!")
    print(f"📊 Router status: {len(orchestrator.list_agents())} agents registered")

    return orchestrator


def demo_llm_routing():
    """Demonstrate DACP's LLM routing capabilities for clients."""
    print(f"\n{'='*60}")
    print("🧠 Demo: LLM Routing Through DACP")
    print("=" * 60)

    orchestrator = demo_independent_client_usage()

    # Test AI analysis routing
    print("\n📨 Client request: AI analysis via DACP routing...")
    response = orchestrator.send_message(
        "client-agent",
        {
            "task": "analyze_with_ai",
            "data": "User engagement metrics: 45% increase in daily active users",
        },
    )
    print(f"🔄 DACP routed response: {response}")


def demo_tool_routing():
    """Demonstrate DACP's tool routing capabilities for clients."""
    print(f"\n{'='*60}")
    print("🔧 Demo: Tool Routing Through DACP")
    print("=" * 60)

    orchestrator = dacp.Orchestrator()
    orchestrator.register_agent("tool-client", ClientAgent())

    # Test file creation routing
    print("\n📨 Client request: File creation via DACP routing...")
    response = orchestrator.send_message(
        "tool-client",
        {
            "task": "create_report",
            "subject": "Market Analysis",
            "content": "Q4 sales exceeded expectations by 23%",
        },
    )
    print(f"🔄 DACP routed response: {response}")

    # Test custom tool routing
    print("\n📨 Client request: Custom tool via DACP routing...")
    response = orchestrator.send_message(
        "tool-client",
        {
            "task": "custom_tool",
            "tool_name": "file_writer",
            "tool_args": {
                "path": "./client_output/custom_file.txt",
                "content": "This file was created via DACP's tool routing system!",
            },
        },
    )
    print(f"🔄 DACP routed response: {response}")


def demo_multi_agent_routing():
    """Demonstrate DACP routing between multiple client agents."""
    print(f"\n{'='*60}")
    print("🎭 Demo: Multi-Agent Routing Through DACP")
    print("=" * 60)

    # Create multiple client agents
    orchestrator = dacp.Orchestrator()

    # Register multiple agents
    agent1 = ClientAgent()
    agent2 = ClientAgent()
    agent3 = ClientAgent()

    orchestrator.register_agent("analytics-agent", agent1)
    orchestrator.register_agent("reporting-agent", agent2)
    orchestrator.register_agent("workflow-agent", agent3)

    print(f"✅ DACP routing for {len(orchestrator.list_agents())} client agents")

    # Test routing to different agents
    agents = ["analytics-agent", "reporting-agent", "workflow-agent"]

    for agent_name in agents:
        print(f"\n📨 Routing to {agent_name}...")
        response = orchestrator.send_message(
            agent_name,
            {
                "task": "analyze_with_ai",
                "data": f"Task routed to {agent_name} via DACP",
            },
        )
        print(
            f"🔄 Response from {agent_name}: {response.get('response', response.get('error'))[:100]}..."
        )

    # Test broadcast routing
    print(f"\n📡 Broadcasting to all agents via DACP...")
    responses = orchestrator.broadcast_message(
        {
            "task": "create_report",
            "subject": "Broadcast Test",
            "content": "This message was broadcast to all agents via DACP routing",
        }
    )

    for agent_name, response in responses.items():
        print(
            f"  📤 {agent_name}: {response.get('tool_result', {}).get('result', {}).get('message', 'No response')}"
        )


def demo_direct_api_usage():
    """Show how clients can use DACP APIs directly without orchestrator."""
    print(f"\n{'='*60}")
    print("🎯 Demo: Direct DACP API Usage")
    print("=" * 60)

    print("\n1️⃣  Direct tool execution...")
    # Client can call tools directly
    result = dacp.execute_tool(
        "file_writer",
        {
            "path": "./direct_api/test.txt",
            "content": "This file was created via direct DACP API call!",
        },
    )
    print(f"🔧 Direct tool result: {result}")

    print("\n2️⃣  Direct intelligence calls...")
    # Client can call LLMs directly (if they have API keys)
    try:
        intelligence_config = {
            "engine": "anthropic",
            "model": "claude-3-haiku-20240307",
            # Would use ANTHROPIC_API_KEY environment variable
        }

        # This would work if API key was set
        print("🧠 Would call: dacp.invoke_intelligence('Hello AI', config)")
        print("   (Skipped - no API key set for demo)")

    except Exception as e:
        print(f"ℹ️  Direct intelligence call: {e}")

    print("\n3️⃣  Direct logging setup...")
    # Client can configure logging directly
    dacp.enable_debug_logging()
    print("🔍 Debug logging enabled via direct DACP API")


def demo_client_tool_registration():
    """Show how clients can register their own custom tools."""
    print(f"\n{'='*60}")
    print("🛠️  Demo: Client Custom Tool Registration")
    print("=" * 60)

    # Client defines their own tool
    def client_custom_tool(args: dict) -> dict:
        """Client's custom business logic tool."""
        name = args.get("name", "unknown")
        value = args.get("value", 0)
        result = f"Client tool processed: {name} with value {value * 2}"
        return {"success": True, "result": result, "processed_value": value * 2}

    # Register with DACP
    print("\n📝 Registering client's custom tool with DACP...")
    dacp.register_tool("client_calculator", client_custom_tool)

    # Use it through orchestrator
    orchestrator = dacp.Orchestrator()
    orchestrator.register_agent("custom-client", ClientAgent())

    print("\n🔧 Using client's custom tool via DACP routing...")
    response = orchestrator.send_message(
        "custom-client",
        {
            "task": "custom_tool",
            "tool_name": "client_calculator",
            "tool_args": {"name": "test_calculation", "value": 21},
        },
    )
    print(f"📊 Custom tool result: {response}")


if __name__ == "__main__":
    print("🎯 DACP Independent Client Integration Demo")
    print("=" * 60)
    print("Showing how clients can use DACP as their agent router")
    print("with zero additional setup beyond: pip install dacp")
    print("=" * 60)

    # Core demos
    demo_llm_routing()
    demo_tool_routing()
    demo_multi_agent_routing()
    demo_direct_api_usage()
    demo_client_tool_registration()

    print(f"\n{'='*60}")
    print("✅ DACP Client Integration Demo Complete!")
    print("=" * 60)

    print("\n🎯 What Clients Get Out of the Box:")
    print("   ✅ Agent registration and routing")
    print("   ✅ Multi-provider LLM access (OpenAI, Anthropic, Azure, Local)")
    print("   ✅ Built-in tool execution (file_writer + custom tools)")
    print("   ✅ Multi-agent orchestration")
    print("   ✅ Conversation history and session management")
    print("   ✅ Comprehensive logging and monitoring")
    print("   ✅ Multi-step workflow support")
    print("   ✅ Broadcast messaging")
    print("   ✅ Error handling and recovery")

    print("\n🚀 Usage Pattern for Clients:")
    print("   1. pip install dacp")
    print("   2. Create agents inheriting from dacp.Agent")
    print("   3. Register agents with dacp.Orchestrator()")
    print("   4. Send messages through orchestrator.send_message()")
    print("   5. DACP handles routing, tools, LLMs, logging automatically!")

    print("\n📋 Files Created During Demo:")
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(".txt") and ("client" in root or "direct" in root):
                print(f"   📄 {os.path.join(root, file)}")
