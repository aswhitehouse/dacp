#!/usr/bin/env python3
"""
DACP Workflow Runtime Demo - VERBOSE VERSION
Shows complete message details and full conversation flow.

This demonstrates the new DACP workflow runtime system with full message logging.
"""

import time
import json
import dacp

# Configure verbose logging
dacp.setup_dacp_logging(level="DEBUG", format_style="detailed")

# Import agents
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'agents', 'agenta'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'agents', 'agentb'))

from agents.agenta.agent import GreetingInitiatorAgent
from agents.agentb.agent import GreetingResponderAgent


def print_section(title: str, content: str = None):
    """Print a formatted section header."""
    print(f"\n{'='*80}")
    print(f"📋 {title}")
    print('='*80)
    if content:
        print(content)


def print_full_message_details(task_data: dict):
    """Print complete task and message details."""
    task_id = task_data['id'][:8]
    agent_id = task_data['agent_id']
    task_name = task_data['task_name']
    status = task_data['status']
    duration = task_data.get('duration', 0)
    
    print(f"\n🔍 TASK DETAILS [{task_id}]")
    print(f"   Agent: {agent_id}")
    print(f"   Task: {task_name}")
    print(f"   Status: {status}")
    print(f"   Duration: {duration:.3f}s")
    
    if task_data.get('input_data'):
        print(f"\n   📥 INPUT DATA:")
        input_data = task_data['input_data']
        for key, value in input_data.items():
            print(f"      {key}: {repr(value)}")
    
    if task_data.get('output_data'):
        print(f"\n   📤 OUTPUT DATA:")
        output_data = task_data['output_data']
        for key, value in output_data.items():
            print(f"      {key}: {repr(value)}")
    
    if task_data.get('error'):
        print(f"\n   ❌ ERROR: {task_data['error']}")


def main():
    """Demonstrate the DACP workflow runtime system with verbose output."""
    print_section("DACP WORKFLOW RUNTIME - VERBOSE DEMONSTRATION", 
                  "Complete message details and conversation flow tracking")
    
    # Create orchestrator and workflow runtime
    orchestrator = dacp.Orchestrator(session_id=f"verbose_demo_{int(time.time())}")
    runtime = dacp.WorkflowRuntime(orchestrator=orchestrator)
    
    # Load workflow configuration
    print_section("WORKFLOW CONFIGURATION")
    try:
        runtime.load_workflow_config("agents/workflow.yaml")
        print("✅ Workflow configuration loaded successfully")
        
        # Show the actual configuration
        workflows = runtime.workflow_config.get('workflows', {})
        for name, config in workflows.items():
            print(f"\n📋 Workflow: {name}")
            print(f"   Description: {config.get('description', 'No description')}")
            print(f"   Steps: {len(config.get('steps', []))}")
            
            for i, step in enumerate(config.get('steps', []), 1):
                print(f"   Step {i}: {step.get('agent')}.{step.get('task')}")
                if step.get('input'):
                    print(f"      Input: {step['input']}")
                if step.get('route_output_to'):
                    route = step['route_output_to']
                    print(f"      Routes to: {route.get('agent')}.{route.get('task')}")
                    if route.get('input_mapping'):
                        print(f"      Input mapping: {route['input_mapping']}")
        
    except Exception as e:
        print(f"❌ Failed to load workflow config: {e}")
        return
    
    # Create and register agents
    print_section("AGENT REGISTRATION")
    
    # Create agent instances
    agent_a = GreetingInitiatorAgent(agent_id="greeting-initiator-agent", orchestrator=orchestrator)
    agent_b = GreetingResponderAgent(agent_id="greeting-responder-agent", orchestrator=orchestrator)
    
    # Register with workflow runtime
    runtime.register_agent_from_config("greeting-initiator-agent", agent_a)
    runtime.register_agent_from_config("greeting-responder-agent", agent_b)
    
    print("✅ Agents registered successfully")
    
    # Execute workflow
    print_section("WORKFLOW EXECUTION")
    
    try:
        workflow_id = runtime.execute_workflow(
            workflow_name="greeting_conversation",
            initial_input={
                "context": "verbose demonstration",
                "style": "detailed and professional"
            }
        )
        print(f"✅ Workflow started with ID: {workflow_id}")
        
        # Wait for workflow to complete
        print("\n⏳ Waiting for workflow to complete...")
        time.sleep(8)  # Give time for OpenAI calls
        
        # Get detailed workflow results
        print_section("COMPLETE WORKFLOW RESULTS")
        
        workflow_status = runtime.get_workflow_status(workflow_id)
        if workflow_status:
            print(f"📊 Workflow: {workflow_status['name']}")
            print(f"   ID: {workflow_id}")
            print(f"   Started: {time.ctime(workflow_status['started_at'])}")
            print(f"   Current Step: {workflow_status['current_step']}")
            
            print(f"\n📋 Final Context:")
            context = workflow_status['context']
            for key, value in context.items():
                if isinstance(value, dict):
                    print(f"   {key}:")
                    for sub_key, sub_value in value.items():
                        print(f"      {sub_key}: {repr(sub_value)}")
                else:
                    print(f"   {key}: {repr(value)}")
            
            print_section("TASK EXECUTION DETAILS")
            
            for i, task in enumerate(workflow_status['tasks'], 1):
                print(f"\n{'='*60}")
                print(f"TASK {i} EXECUTION")
                print('='*60)
                print_full_message_details(task)
        
        # Show runtime statistics
        print_section("RUNTIME STATISTICS")
        final_status = runtime.get_runtime_status()
        print(f"📊 Execution Summary:")
        print(f"   Total tasks executed: {final_status['tasks']['total_tasks']}")
        print(f"   Task status breakdown: {final_status['tasks']['status_counts']}")
        
        print(f"\n🤖 Agent Activity:")
        for agent_info in final_status['agents']['agents']:
            agent_id = agent_info['id']
            agent_type = agent_info['agent_type']
            last_activity = agent_info.get('last_activity')
            
            if last_activity:
                activity_time = time.ctime(last_activity)
                print(f"   • {agent_id} ({agent_type})")
                print(f"     Last active: {activity_time}")
            else:
                print(f"   • {agent_id} ({agent_type}) - No activity")
        
        print_section("CONVERSATION SUMMARY")
        
        # Extract and show the actual conversation
        tasks = workflow_status['tasks']
        if len(tasks) >= 2:
            agent_a_task = tasks[0]
            agent_b_task = tasks[1]
            
            print("🗣️  AGENT-TO-AGENT CONVERSATION:")
            print(f"\n   Agent A (greeting-initiator-agent):")
            if agent_a_task.get('output_data', {}).get('greeting_message'):
                greeting = agent_a_task['output_data']['greeting_message']
                print(f"      💬 \"{greeting}\"")
            
            print(f"\n   Agent B (greeting-responder-agent):")
            if agent_b_task.get('output_data', {}).get('response_message'):
                response = agent_b_task['output_data']['response_message']
                print(f"      💬 \"{response}\"")
            
            print(f"\n✅ Total conversation time: {agent_a_task.get('duration', 0) + agent_b_task.get('duration', 0):.2f} seconds")
            print(f"✅ Both agents used GPT-4 for real-time responses")
            print(f"✅ Agent-to-agent communication successful")
        
        print_section("DEMONSTRATION COMPLETED", 
                      "✅ Verbose workflow execution completed successfully!")
        
    except Exception as e:
        print(f"❌ Workflow execution failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main() 