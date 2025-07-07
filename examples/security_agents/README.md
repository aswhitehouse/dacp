# Security Workflow Demo - DACP Example

This example demonstrates a real-world security use case using DACP workflow orchestration with two specialized security agents communicating to analyze threats and assess organizational risk.

## Overview

**Workflow Flow:**
1. **Threat Analyzer Agent** - Analyzes security events for potential threats
2. **Risk Assessor Agent** - Evaluates threats and provides risk scores + actionable recommendations
3. **DACP Orchestration** - Manages agent-to-agent communication and data flow

## Files

- `security_workflow_demo.py` - Main demonstration script
- `threat-analyzer.yaml` - OAS specification for threat detection agent
- `risk-assessor.yaml` - OAS specification for risk assessment agent  
- `security-workflow.yaml` - DACP workflow configuration
- `README.md` - This documentation

## Prerequisites

1. **Install Dependencies:**
   ```bash
   pip install dacp anthropic open-agent-spec
   ```

2. **Generate Agents (Optional - for live demo):**
   ```bash
   # Generate threat analyzer
   oas init --spec threat-analyzer.yaml --output threat-analyzer/
   
   # Generate risk assessor
   oas init --spec risk-assessor.yaml --output risk-assessor/
   ```

3. **Configure API Keys (if running live agents):**
   ```bash
   # Add to threat-analyzer/.env and risk-assessor/.env
   ANTHROPIC_API_KEY=your-api-key-here
   ```

## Running the Demo

### Simulation Mode (No API Keys Required)
```bash
python security_workflow_demo.py
```

This runs a complete simulation showing:
- Realistic security incident analysis
- Agent-to-agent communication patterns
- DACP workflow orchestration
- Structured threat assessment outputs

### Live Agent Mode (Requires Generated Agents + API Keys)
```bash
# After generating agents and configuring API keys
python security_workflow_demo.py
```

## Example Output

```
🛡️  DACP SECURITY WORKFLOW DEMONSTRATION
======================================================================
Two-stage security analysis: Threat Detection → Risk Assessment

🛡️  SIMULATED STAGE 1: THREAT ANALYSIS
======================================================================
✅ [SIMULATED] Threat analysis completed!
   🚨 Threat Identified: True
   🏷️  Threat Type: brute_force
   ⚠️  Severity: high
   📋 Indicators: Multiple failed login attempts, Admin account targeted, Short time window
   📝 Summary: Brute force attack detected against admin account from single IP address

🛡️  SIMULATED STAGE 2: RISK ASSESSMENT
======================================================================
✅ [SIMULATED] Risk assessment completed!
   📊 Risk Score: 8.5/10
   🏷️  Risk Level: HIGH
   💼 Business Impact: Potential unauthorized access to critical customer database with PII data
   🚨 Escalation Required: True
   📈 Confidence Level: 0.92

   ⚡ Immediate Actions:
      1. Immediately block source IP 192.168.1.100
      2. Reset admin account password
      3. Enable enhanced monitoring for admin accounts
      4. Review recent admin account activity

   🛡️  Mitigation Recommendations:
      1. Implement multi-factor authentication for admin accounts
      2. Deploy account lockout policies with progressive delays
      3. Set up real-time alerting for multiple failed logins
      4. Conduct security awareness training for admin users
```

## DACP Features Demonstrated

- **Multi-Agent Orchestration** - Coordinating specialized security agents
- **Agent-to-Agent Communication** - Threat analysis data flows to risk assessment
- **Workflow Configuration** - YAML-defined agent interaction patterns
- **Real-time Processing** - Live security incident analysis pipeline
- **Structured Data Flow** - JSON communication between agents with validation

## Security Agent Patterns

### Threat Analyzer
- **Input**: Security events (failed logins, port scans, data access, etc.)
- **Output**: Threat identification, type classification, severity assessment
- **Behavioral Contract**: High conservatism, detailed analysis, strict temperature control

### Risk Assessor  
- **Input**: Threat analysis results + asset context
- **Output**: Risk scores, business impact, immediate actions, mitigation recommendations
- **Behavioral Contract**: Comprehensive evaluation, practical recommendations, safety checks

## Integration with Open Agent Stack

This example showcases the complete **OAS + BC + DACP** ecosystem:

- **OAS (Open Agent Spec)** - Declarative agent definitions via YAML
- **BC (Behavioral Contracts)** - Governance and validation using decorators  
- **DACP** - Runtime orchestration and agent communication

## Use Cases

This pattern can be adapted for various security scenarios:

- **Incident Response** - Automated threat analysis and response planning
- **SOC Operations** - Multi-stage security event processing
- **Risk Management** - Continuous threat assessment and mitigation planning
- **Compliance Monitoring** - Automated security control evaluation

## Learn More

- **DACP Documentation** - [dacp.ai](https://dacp.ai)
- **Open Agent Stack** - [openagentstack.ai](https://openagentstack.ai)
- **Guardian AI Project** - Real-world security agent implementations