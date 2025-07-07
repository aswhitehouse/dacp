#!/usr/bin/env python3
"""
DACP Security Workflow Demo

This demonstrates a real-world security use case with DACP workflow orchestration:
- Threat Analyzer Agent: Analyzes security events for potential threats
- Risk Assessor Agent: Evaluates threats and provides risk scores + recommendations
- Agent-to-Agent Communication: Shows data flow between specialized security agents

This example showcases how DACP can orchestrate multi-agent security analysis
pipelines, demonstrating practical agent communication patterns.
"""

import time
import json
import os
import sys
import importlib.util

# Import DACP for workflow orchestration
import dacp


def print_section(title: str, content: str = None):
    """Print a formatted section header."""
    print(f"\n{'='*70}")
    print(f"🛡️  {title}")
    print('='*70)
    if content:
        print(content)


def create_security_incident_test_data():
    """Create realistic security incident test data."""
    return {
        "event_type": "multiple_failed_logins",
        "event_details": "User account 'admin' had 15 failed login attempts from IP 192.168.1.100 within 5 minutes. Account is now locked.",
        "source_ip": "192.168.1.100", 
        "timestamp": "2024-01-15T14:30:00Z",
        "asset_context": "Critical customer database server with PII data"
    }


def load_agent_from_file(file_path: str, class_name: str):
    """Dynamically load an agent class from a file."""
    spec = importlib.util.spec_from_file_location("agent_module", file_path)
    agent_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(agent_module)
    return getattr(agent_module, class_name)


def main():
    """Demonstrate DACP security workflow with agent-to-agent communication."""
    print_section("DACP SECURITY WORKFLOW DEMONSTRATION", 
                  "Two-stage security analysis: Threat Detection → Risk Assessment")
    
    # Create orchestrator for workflow management
    orchestrator = dacp.Orchestrator(session_id=f"security_demo_{int(time.time())}")
    
    print_section("AGENT INITIALIZATION")
    print("📋 This demo requires OAS-generated security agents.")
    print("📋 To run this demo:")
    print("   1. Generate threat-analyzer and risk-assessor agents using OAS")
    print("   2. Place them in the examples/ directory")
    print("   3. Configure API keys in .env files")
    print("")
    print("🔧 Agent Specifications Available:")
    print("   - threat-analyzer.yaml: Security event analysis agent")
    print("   - risk-assessor.yaml: Risk evaluation and recommendation agent")
    
    # Check if agent files exist (they would be copied here in a real implementation)
    threat_analyzer_path = "examples/threat-analyzer/agent.py"
    risk_assessor_path = "examples/risk-assessor/agent.py"
    
    if not (os.path.exists(threat_analyzer_path) and os.path.exists(risk_assessor_path)):
        print_section("DEMO SIMULATION")
        print("⚠️  Agent files not found - running simulation mode")
        
        # Simulate the workflow results
        print_section("SIMULATED SECURITY INCIDENT DATA")
        test_incident = create_security_incident_test_data()
        print(f"📊 Event Type: {test_incident['event_type']}")
        print(f"📊 Source IP: {test_incident['source_ip']}")
        print(f"📊 Timestamp: {test_incident['timestamp']}")
        print(f"📊 Details: {test_incident['event_details']}")
        print(f"📊 Asset Context: {test_incident['asset_context']}")
        
        print_section("SIMULATED STAGE 1: THREAT ANALYSIS")
        print("🔍 [SIMULATED] Threat Analyzer processing security event...")
        simulated_threat_result = {
            "threat_identified": True,
            "threat_type": "brute_force",
            "threat_severity": "high",
            "threat_indicators": ["Multiple failed login attempts", "Admin account targeted", "Short time window"],
            "analysis_summary": "Brute force attack detected against admin account from single IP address"
        }
        
        time.sleep(1)  # Simulate processing time
        print("✅ [SIMULATED] Threat analysis completed!")
        print(f"   🚨 Threat Identified: {simulated_threat_result['threat_identified']}")
        print(f"   🏷️  Threat Type: {simulated_threat_result['threat_type']}")
        print(f"   ⚠️  Severity: {simulated_threat_result['threat_severity']}")
        print(f"   📋 Indicators: {', '.join(simulated_threat_result['threat_indicators'])}")
        print(f"   📝 Summary: {simulated_threat_result['analysis_summary']}")
        
        print_section("SIMULATED STAGE 2: RISK ASSESSMENT")
        print("⚖️  [SIMULATED] Risk Assessor evaluating threat...")
        simulated_risk_result = {
            "risk_score": 8.5,
            "risk_level": "high",
            "business_impact": "Potential unauthorized access to critical customer database with PII data",
            "immediate_actions": [
                "Immediately block source IP 192.168.1.100",
                "Reset admin account password",
                "Enable enhanced monitoring for admin accounts",
                "Review recent admin account activity"
            ],
            "mitigation_recommendations": [
                "Implement multi-factor authentication for admin accounts",
                "Deploy account lockout policies with progressive delays",
                "Set up real-time alerting for multiple failed logins",
                "Conduct security awareness training for admin users"
            ],
            "escalation_required": True,
            "confidence_level": 0.92
        }
        
        time.sleep(1)  # Simulate processing time
        print("✅ [SIMULATED] Risk assessment completed!")
        print(f"   📊 Risk Score: {simulated_risk_result['risk_score']}/10")
        print(f"   🏷️  Risk Level: {simulated_risk_result['risk_level'].upper()}")
        print(f"   💼 Business Impact: {simulated_risk_result['business_impact']}")
        print(f"   🚨 Escalation Required: {simulated_risk_result['escalation_required']}")
        print(f"   📈 Confidence Level: {simulated_risk_result['confidence_level']:.2f}")
        
        print(f"\n   ⚡ Immediate Actions:")
        for i, action in enumerate(simulated_risk_result['immediate_actions'], 1):
            print(f"      {i}. {action}")
        
        print(f"\n   🛡️  Mitigation Recommendations:")
        for i, recommendation in enumerate(simulated_risk_result['mitigation_recommendations'], 1):
            print(f"      {i}. {recommendation}")
        
        print_section("WORKFLOW SUMMARY")
        print("🔄 DACP Agent-to-Agent Communication Flow:")
        print("   1. Threat Analyzer → Analyzed security event")
        print("   2. DACP Runtime → Routed threat analysis to Risk Assessor")
        print("   3. Risk Assessor → Generated comprehensive risk assessment")
        print("   4. DACP Orchestrator → Coordinated data flow between agents")
        
        print(f"\n📋 Final Security Assessment:")
        print(f"   • Threat: {simulated_threat_result['threat_type']} ({simulated_threat_result['threat_severity']})")
        print(f"   • Risk: {simulated_risk_result['risk_score']}/10 ({simulated_risk_result['risk_level'].upper()})")
        print(f"   • Escalation: {'YES' if simulated_risk_result['escalation_required'] else 'NO'}")
        print(f"   • Actions: {len(simulated_risk_result['immediate_actions'])} immediate, {len(simulated_risk_result['mitigation_recommendations'])} mitigation")
        
        print_section("DEMO TECHNICAL DETAILS")
        print("🔧 This demo showcases DACP's capabilities for:")
        print("   • Multi-agent workflow orchestration")
        print("   • Agent-to-agent data flow management") 
        print("   • Real-time security analysis pipelines")
        print("   • Structured JSON communication between agents")
        print("   • Behavioral contract enforcement across agents")
        
        print("\n🎯 Real Implementation Requirements:")
        print("   • OAS-generated threat-analyzer and risk-assessor agents")
        print("   • Claude or OpenAI API keys configured")
        print("   • DACP workflow.yaml configuration file")
        print("   • Behavioral contracts for security analysis validation")
        
    else:
        # This would be the real implementation if agents were present
        print("🚀 Loading OAS-generated security agents...")
        
        # Load the actual agents (when available)
        ThreatAnalyzerAgent = load_agent_from_file(threat_analyzer_path, "ThreatAnalyzerAgent")
        RiskAssessorAgent = load_agent_from_file(risk_assessor_path, "RiskAssessorAgent")
        
        # Create agent instances
        threat_analyzer = ThreatAnalyzerAgent(agent_id="threat-analyzer", orchestrator=orchestrator)
        risk_assessor = RiskAssessorAgent(agent_id="risk-assessor", orchestrator=orchestrator)
        
        # Run the actual workflow (implementation would be similar to simulation above)
        print("✅ Real agents loaded - executing live workflow...")
    
    print_section("DEMONSTRATION COMPLETED",
                  "✅ DACP security workflow demonstration finished!")
    print("\n📖 For more DACP examples, see: examples/")
    print("🔗 Learn more about Open Agent Stack: https://openagentstack.ai")


if __name__ == "__main__":
    main()