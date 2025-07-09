#!/usr/bin/env python3
"""
DACP Multi-Step Workflow Demo

This demonstrates how DACP handles complex multi-step tasks that OAS agents
would typically need to perform. Shows conversation state, tool chaining,
and intelligent workflow management.
"""

import dacp
import os
import time


class MultiStepAgent(dacp.Agent):
    """
    A sophisticated agent that demonstrates multi-step workflows typical
    of Open Agent Spec (OAS) agents.
    """

    def __init__(self):
        self.workflow_state = {}
        self.step_counter = 0

    def handle_message(self, message):
        """Handle complex multi-step tasks."""
        task = message.get("task")
        workflow_id = message.get("workflow_id", "default")

        # Initialize workflow state if needed
        if workflow_id not in self.workflow_state:
            self.workflow_state[workflow_id] = {
                "started_at": time.time(),
                "steps_completed": [],
                "data": {},
                "current_step": 0,
            }

        state = self.workflow_state[workflow_id]

        if task == "analyze_project":
            return self._start_project_analysis_workflow(message, state)
        elif task == "continue_workflow":
            return self._continue_workflow(message, state)
        elif task == "get_workflow_status":
            return self._get_workflow_status(workflow_id, state)
        elif task == "multi_step_research":
            return self._handle_research_workflow(message, state)
        else:
            return {"error": f"Unknown task: {task}"}

    def _start_project_analysis_workflow(self, message, state):
        """Start a multi-step project analysis workflow."""
        project_name = message.get("project_name", "Unknown Project")

        # Step 1: Gather initial information
        if state["current_step"] == 0:
            state["current_step"] = 1
            state["data"]["project_name"] = project_name
            state["steps_completed"].append("initialization")

            # Request project file creation
            return {
                "workflow_status": "in_progress",
                "current_step": "creating_project_structure",
                "tool_request": {
                    "name": "file_writer",
                    "args": {
                        "path": f"./projects/{project_name}/analysis.md",
                        "content": f"# Project Analysis: {project_name}\n\nStarted at: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n## Analysis Steps:\n1. ✅ Project structure created\n2. ⏳ Gathering requirements\n3. ⏳ Technical analysis\n4. ⏳ Risk assessment\n5. ⏳ Final report\n",
                    },
                },
            }

        # Continue workflow with next steps
        return self._continue_workflow(message, state)

    def _continue_workflow(self, message, state):
        """Continue multi-step workflow based on current state."""
        current_step = state["current_step"]

        if current_step == 1:
            # Step 2: Gather requirements
            state["current_step"] = 2
            state["steps_completed"].append("project_structure")

            return {
                "workflow_status": "in_progress",
                "current_step": "requirements_analysis",
                "intelligence_request": {
                    "prompt": f"Analyze the requirements for a project named '{state['data']['project_name']}'. What key requirements should we consider?",
                    "purpose": "requirements_gathering",
                },
                "response": "Requirements analysis phase started. Using AI to gather comprehensive requirements.",
            }

        elif current_step == 2:
            # Step 3: Technical analysis
            state["current_step"] = 3
            state["steps_completed"].append("requirements")

            # Simulate storing requirements from previous intelligence call
            state["data"]["requirements"] = message.get(
                "ai_response", "Standard project requirements"
            )

            return {
                "workflow_status": "in_progress",
                "current_step": "technical_analysis",
                "tool_request": {
                    "name": "file_writer",
                    "args": {
                        "path": f"./projects/{state['data']['project_name']}/technical_analysis.md",
                        "content": f"# Technical Analysis\n\n## Requirements:\n{state['data']['requirements']}\n\n## Technical Considerations:\n- Architecture planning needed\n- Technology stack evaluation\n- Performance requirements\n- Scalability factors\n",
                    },
                },
            }

        elif current_step == 3:
            # Step 4: Risk assessment
            state["current_step"] = 4
            state["steps_completed"].append("technical_analysis")

            return {
                "workflow_status": "in_progress",
                "current_step": "risk_assessment",
                "intelligence_request": {
                    "prompt": f"Perform a risk assessment for project '{state['data']['project_name']}' with requirements: {state['data'].get('requirements', 'N/A')}",
                    "purpose": "risk_analysis",
                },
                "response": "Conducting AI-powered risk assessment analysis.",
            }

        elif current_step == 4:
            # Step 5: Final report
            state["current_step"] = 5
            state["steps_completed"].append("risk_assessment")
            state["data"]["risks"] = message.get("ai_response", "Standard project risks identified")

            duration = time.time() - state["started_at"]

            return {
                "workflow_status": "completing",
                "current_step": "final_report",
                "tool_request": {
                    "name": "file_writer",
                    "args": {
                        "path": f"./projects/{state['data']['project_name']}/final_report.md",
                        "content": f"# Final Project Analysis Report\n\n**Project:** {state['data']['project_name']}\n**Analysis Duration:** {duration:.1f} seconds\n**Steps Completed:** {len(state['steps_completed'])}\n\n## Requirements:\n{state['data'].get('requirements', 'N/A')}\n\n## Risk Assessment:\n{state['data']['risks']}\n\n## Conclusion:\nProject analysis completed successfully.\n",
                    },
                },
            }

        else:
            # Workflow complete
            state["current_step"] = "completed"
            duration = time.time() - state["started_at"]

            return {
                "workflow_status": "completed",
                "response": f"Multi-step project analysis completed! Duration: {duration:.1f}s, Steps: {len(state['steps_completed'])}",
                "summary": {
                    "project_name": state["data"]["project_name"],
                    "steps_completed": state["steps_completed"],
                    "duration": duration,
                    "files_created": [
                        f"./projects/{state['data']['project_name']}/analysis.md",
                        f"./projects/{state['data']['project_name']}/technical_analysis.md",
                        f"./projects/{state['data']['project_name']}/final_report.md",
                    ],
                },
            }

    def _handle_research_workflow(self, message, state):
        """Handle a multi-step research workflow."""
        topic = message.get("topic", "AI Research")

        if state["current_step"] == 0:
            state["current_step"] = 1
            state["data"]["topic"] = topic

            return {
                "workflow_status": "starting_research",
                "intelligence_request": {
                    "prompt": f"Create a research outline for the topic: {topic}. Provide 5 key areas to investigate.",
                    "purpose": "research_planning",
                },
                "response": f"Starting research on: {topic}",
            }

        elif state["current_step"] == 1:
            state["current_step"] = 2
            outline = message.get("ai_response", "Research outline not available")
            state["data"]["outline"] = outline

            return {
                "workflow_status": "gathering_sources",
                "tool_request": {
                    "name": "file_writer",
                    "args": {
                        "path": f"./research/{topic.replace(' ', '_')}_outline.md",
                        "content": f"# Research Outline: {topic}\n\n{outline}\n\n## Research Progress:\n- ✅ Outline created\n- ⏳ Source gathering\n- ⏳ Analysis\n- ⏳ Final report\n",
                    },
                },
            }

        else:
            return {
                "workflow_status": "completed",
                "response": f"Research workflow for '{topic}' completed with outline and initial documentation.",
            }

    def _get_workflow_status(self, workflow_id, state):
        """Get current status of a workflow."""
        return {
            "workflow_id": workflow_id,
            "current_step": state["current_step"],
            "steps_completed": state["steps_completed"],
            "duration": time.time() - state["started_at"],
            "data_keys": list(state["data"].keys()),
        }


def demo_multi_step_workflow():
    """Demonstrate complex multi-step workflows."""
    print("🚀 DACP Multi-Step Workflow Demo\n")

    # Enable detailed logging to see all steps
    dacp.enable_info_logging()

    # Create orchestrator and agent
    orchestrator = dacp.Orchestrator()
    agent = MultiStepAgent()
    orchestrator.register_agent("workflow-agent", agent)

    print("=" * 60)
    print("📋 Demo 1: Project Analysis Workflow")
    print("=" * 60)

    # Start multi-step project analysis
    workflow_id = "project_001"

    # Step 1: Start workflow
    print("\n🔄 Step 1: Starting project analysis...")
    response = orchestrator.send_message(
        "workflow-agent",
        {
            "task": "analyze_project",
            "project_name": "DACP Integration",
            "workflow_id": workflow_id,
        },
    )
    print(f"Response: {response}")

    # Step 2: Continue workflow (simulating tool completion)
    print("\n🔄 Step 2: Continuing workflow...")
    response = orchestrator.send_message(
        "workflow-agent", {"task": "continue_workflow", "workflow_id": workflow_id}
    )
    print(f"Response: {response}")

    # Step 3: Continue with AI response simulation
    print("\n🔄 Step 3: Continuing with requirements...")
    response = orchestrator.send_message(
        "workflow-agent",
        {
            "task": "continue_workflow",
            "workflow_id": workflow_id,
            "ai_response": "Requirements: Seamless OAS integration, comprehensive logging, multi-provider support",
        },
    )
    print(f"Response: {response}")

    # Step 4: Continue workflow
    print("\n🔄 Step 4: Technical analysis phase...")
    response = orchestrator.send_message(
        "workflow-agent", {"task": "continue_workflow", "workflow_id": workflow_id}
    )
    print(f"Response: {response}")

    # Step 5: Risk assessment with AI response
    print("\n🔄 Step 5: Risk assessment...")
    response = orchestrator.send_message(
        "workflow-agent",
        {
            "task": "continue_workflow",
            "workflow_id": workflow_id,
            "ai_response": "Risks: API rate limits, dependency compatibility, configuration complexity",
        },
    )
    print(f"Response: {response}")

    # Final step: Complete workflow
    print("\n🔄 Final Step: Completing workflow...")
    response = orchestrator.send_message(
        "workflow-agent", {"task": "continue_workflow", "workflow_id": workflow_id}
    )
    print(f"Final Response: {response}")

    # Check workflow status
    print("\n📊 Workflow Status:")
    status = orchestrator.send_message(
        "workflow-agent", {"task": "get_workflow_status", "workflow_id": workflow_id}
    )
    print(f"Status: {status}")


def demo_research_workflow():
    """Demonstrate research workflow."""
    print(f"\n{'=' * 60}")
    print("📚 Demo 2: Research Workflow")
    print("=" * 60)

    orchestrator = dacp.Orchestrator()
    agent = MultiStepAgent()
    orchestrator.register_agent("research-agent", agent)

    # Start research workflow
    print("\n🔍 Starting research workflow...")
    response = orchestrator.send_message(
        "research-agent",
        {
            "task": "multi_step_research",
            "topic": "AI Agent Orchestration",
            "workflow_id": "research_001",
        },
    )
    print(f"Response: {response}")

    # Continue with research outline
    print("\n🔍 Continuing research with AI outline...")
    response = orchestrator.send_message(
        "research-agent",
        {
            "task": "multi_step_research",  # Use the correct task
            "topic": "AI Agent Orchestration",
            "workflow_id": "research_001",
            "ai_response": "1. Agent Communication Protocols\n2. Tool Integration Patterns\n3. State Management\n4. Error Handling\n5. Performance Optimization",
        },
    )
    print(f"Response: {response}")


def demo_conversation_history():
    """Demonstrate conversation history tracking."""
    print(f"\n{'=' * 60}")
    print("📜 Demo 3: Conversation History")
    print("=" * 60)

    orchestrator = dacp.Orchestrator()
    agent = MultiStepAgent()
    orchestrator.register_agent("history-agent", agent)

    # Send several messages
    messages = [
        {
            "task": "analyze_project",
            "project_name": "Test Project",
            "workflow_id": "hist_001",
        },
        {"task": "continue_workflow", "workflow_id": "hist_001"},
        {"task": "get_workflow_status", "workflow_id": "hist_001"},
    ]

    for i, msg in enumerate(messages, 1):
        print(f"\n📨 Message {i}: {msg}")
        response = orchestrator.send_message("history-agent", msg)
        print(f"Response {i}: {response}")

    # Show conversation history
    print(f"\n📚 Conversation History:")
    history = orchestrator.get_conversation_history()
    for i, entry in enumerate(history, 1):
        print(
            f"  Entry {i}: {entry['agent_name']} - {entry['message'].get('task')} -> {entry['response'].get('workflow_status', 'N/A')} ({entry['duration']:.3f}s)"
        )


if __name__ == "__main__":
    demo_multi_step_workflow()
    demo_research_workflow()
    demo_conversation_history()

    print(f"\n{'=' * 60}")
    print("✅ Multi-Step Workflow Demo Complete!")
    print("=" * 60)
    print("\n🎯 Key DACP Features Demonstrated:")
    print("   ✅ Multi-step task orchestration")
    print("   ✅ Workflow state management")
    print("   ✅ Tool chaining and execution")
    print("   ✅ Intelligence integration points")
    print("   ✅ Conversation history tracking")
    print("   ✅ Session management")
    print("   ✅ Comprehensive logging")
    print("\n🚀 DACP is ready for complex OAS agent workflows!")
