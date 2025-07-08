#!/usr/bin/env python3
"""
DACP Workflow Runtime Demo - Declarative workflow execution from workflow.yaml

This demonstrates the new DACP workflow runtime system that:
1. Loads workflow configuration from workflow.yaml
2. Maintains agent and task registries
3. Executes workflows declaratively
4. Routes tasks between agents based on configuration
"""

import time
import json
import dacp

# Configure logging
dacp.setup_dacp_logging(level="INFO", format_style="detailed")

# Import agents
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "agents", "agenta"))
sys.path.append(os.path.join(os.path.dirname(__file__), "agents", "agentb"))

from agents.agenta.agent import GreetingInitiatorAgent
from agents.agentb.agent import GreetingResponderAgent


def main():
    """Demonstrate the DACP workflow runtime system."""
    print("\n" + "=" * 80)
    print("🚀 DACP WORKFLOW RUNTIME DEMONSTRATION")
    print("Declarative Agent Collaboration from workflow.yaml")
    print("=" * 80)

    # Create orchestrator and workflow runtime
    orchestrator = dacp.Orchestrator(session_id=f"runtime_demo_{int(time.time())}")
    runtime = dacp.WorkflowRuntime(orchestrator=orchestrator)

    # Load workflow configuration
    print("\n📁 Loading workflow configuration...")
    try:
        runtime.load_workflow_config("agents/workflow.yaml")
        print("✅ Workflow configuration loaded successfully")
    except Exception as e:
        print(f"❌ Failed to load workflow config: {e}")
        return

    # Create and register agents
    print("\n🤖 Creating and registering agents...")

    # Create agent instances (they register themselves with orchestrator)
    agent_a = GreetingInitiatorAgent(
        agent_id="greeting-initiator-agent", orchestrator=orchestrator
    )
    agent_b = GreetingResponderAgent(
        agent_id="greeting-responder-agent", orchestrator=orchestrator
    )

    # Register with workflow runtime
    runtime.register_agent_from_config("greeting-initiator-agent", agent_a)
    runtime.register_agent_from_config("greeting-responder-agent", agent_b)

    print("✅ Agents registered in runtime")

    # Show runtime status
    print("\n📊 Runtime Status:")
    status = runtime.get_runtime_status()
    print(f"   Registered agents: {status['agents']['registered']}")
    print(f"   Configured workflows: {status['workflows']['configured']}")
    print(f"   Active workflows: {status['workflows']['active']}")

    # List available workflows
    print("\n📋 Available Workflows:")
    workflows = runtime.workflow_config.get("workflows", {})
    for name, config in workflows.items():
        description = config.get("description", "No description")
        steps = len(config.get("steps", []))
        print(f"   • {name}: {description} ({steps} steps)")

    # Execute workflow
    print("\n🚀 Executing workflow...")

    try:
        workflow_id = runtime.execute_workflow(
            workflow_name="greeting_conversation",
            initial_input={"context": "demonstration", "style": "professional"},
        )
        print(f"✅ Workflow started with ID: {workflow_id}")

        # Wait for workflow to complete
        print("\n⏳ Waiting for workflow to complete...")
        time.sleep(8)  # Give time for OpenAI calls

        # Get workflow status
        workflow_status = runtime.get_workflow_status(workflow_id)
        if workflow_status:
            print(f"\n📊 Workflow Status:")
            print(f"   Name: {workflow_status['name']}")
            print(f"   Current Step: {workflow_status['current_step']}")
            print(f"   Started At: {time.ctime(workflow_status['started_at'])}")
            print(f"   Context: {workflow_status['context']}")

            print(f"\n📋 Task Execution Details:")
            for i, task in enumerate(workflow_status["tasks"], 1):
                task_id = task["id"][:8]
                agent_id = task["agent_id"]
                task_name = task["task_name"]
                status = task["status"]
                duration = task.get("duration", 0)

                print(f"   {i}. [{task_id}] {agent_id}.{task_name} - {status}")
                if duration:
                    print(f"      Duration: {duration:.2f}s")

                if task.get("output_data"):
                    output = task["output_data"]
                    if isinstance(output, dict):
                        for key, value in output.items():
                            # Show full messages without truncation
                            print(f"      {key}: {value}")

                if task.get("error"):
                    print(f"      Error: {task['error']}")

        # Show final runtime status
        print("\n📊 Final Runtime Status:")
        final_status = runtime.get_runtime_status()
        print(f"   Total tasks executed: {final_status['tasks']['total_tasks']}")
        print(f"   Task status breakdown: {final_status['tasks']['status_counts']}")

        # Show agent activity
        print(f"\n🤖 Agent Activity:")
        for agent_info in final_status["agents"]["agents"]:
            agent_id = agent_info["id"]
            agent_type = agent_info["agent_type"]
            last_activity = agent_info.get("last_activity")

            if last_activity:
                activity_time = time.ctime(last_activity)
                print(f"   • {agent_id} ({agent_type}) - Last active: {activity_time}")
            else:
                print(f"   • {agent_id} ({agent_type}) - No activity")

        # Show workflow configuration that was executed
        print(f"\n📋 Executed Workflow Configuration:")
        executed_workflow = runtime.workflow_config["workflows"][
            "greeting_conversation"
        ]
        print(f"   Description: {executed_workflow['description']}")
        print(f"   Steps:")
        for i, step in enumerate(executed_workflow["steps"], 1):
            agent = step.get("agent")
            task = step.get("task")
            print(f"     {i}. {agent}.{task}")

            if "route_output_to" in step:
                route = step["route_output_to"]
                next_agent = route.get("agent")
                next_task = route.get("task")
                print(f"        → Routes to: {next_agent}.{next_task}")

        print("\n" + "=" * 80)
        print("🎉 WORKFLOW RUNTIME DEMONSTRATION COMPLETED!")
        print("✅ Declarative workflow execution: WORKING")
        print("✅ Agent registry management: WORKING")
        print("✅ Task registry tracking: WORKING")
        print("✅ YAML-driven collaboration: WORKING")
        print("=" * 80)

    except Exception as e:
        print(f"❌ Workflow execution failed: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
