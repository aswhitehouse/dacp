# 3-Stage Security Workflow Demo - DACP Example

This example demonstrates a comprehensive security operations workflow using DACP orchestration with three specialized security agents working together to provide end-to-end incident response.

## Overview

**Complete Security Pipeline:**
1. **Threat Analyzer Agent** - Analyzes security events for potential threats (Claude-powered)
2. **Risk Assessor Agent** - Evaluates threats and provides risk scores + actionable recommendations (Claude-powered)
3. **Incident Responder Agent** - Coordinates incident response when risk threshold exceeded (OpenAI-powered)
4. **DACP Orchestration** - Manages agent-to-agent communication and conditional workflow routing

**Key Features:**
- **Multi-Engine Integration** - Claude + OpenAI working together seamlessly
- **Conditional Escalation** - Stage 3 triggers when risk ≥ 7.0 or escalation required
- **Production-Ready** - Real SOC (Security Operations Center) automation patterns

## Files

- `security_workflow_demo.py` - Complete 3-stage demonstration script
- `threat-analyzer.yaml` - OAS specification for threat detection agent (Claude)
- `risk-assessor.yaml` - OAS specification for risk assessment agent (Claude)
- `incident-responder.yaml` - OAS specification for incident response agent (OpenAI)
- `security-workflow.yaml` - DACP workflow configuration with 3-stage pipeline
- `README.md` - This documentation

## Prerequisites

1. **Install Dependencies:**
   ```bash
   pip install dacp anthropic openai open-agent-spec
   ```

2. **Generate Agents (Optional - for live demo):**
   ```bash
   # Generate threat analyzer (Claude-powered)
   oas init --spec threat-analyzer.yaml --output threat-analyzer/
   
   # Generate risk assessor (Claude-powered)
   oas init --spec risk-assessor.yaml --output risk-assessor/
   
   # Generate incident responder (OpenAI-powered)
   oas init --spec incident-responder.yaml --output incident-responder/
   ```

3. **Configure API Keys (if running live agents):**
   ```bash
   # For Claude-powered agents
   echo "ANTHROPIC_API_KEY=your-anthropic-key" > threat-analyzer/.env
   echo "ANTHROPIC_API_KEY=your-anthropic-key" > risk-assessor/.env
   
   # For OpenAI-powered agents
   echo "OPENAI_API_KEY=your-openai-key" > incident-responder/.env
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
🛡️  3-STAGE SECURITY WORKFLOW DEMONSTRATION
======================================================================
Comprehensive security analysis: Threat Analysis → Risk Assessment → Incident Response

🛡️  STAGE 1: THREAT ANALYSIS
======================================================================
✅ Threat analysis completed!
   🚨 Threat Identified: True
   🏷️  Threat Type: sql_injection
   ⚠️  Severity: critical
   📋 Indicators: sql_injection, data_breach, unauthorized_access, botnet_activity
   📝 Summary: Critical data breach in progress from known botnet IP...

🛡️  STAGE 2: RISK ASSESSMENT
======================================================================
✅ Risk assessment completed!
   📊 Risk Score: 9.8/10
   🏷️  Risk Level: CRITICAL
   💼 Business Impact: Active breach of regulated PII data affecting 50k+ customers...
   🚨 Escalation Required: True
   📈 Confidence Level: 0.95

   ⚡ Immediate Actions:
      1. Isolate affected systems and block malicious IP
      2. Engage incident response team
      3. Stop data exfiltration by blocking outbound traffic

🛡️  STAGE 3: INCIDENT RESPONSE COORDINATION
======================================================================
✅ Incident response coordination completed!
   🆔 Incident ID: INC-2024-0001
   ⏱️  Timeline: 24-48 hours for containment, 72 hours for full investigation
   📋 Response Plan: 5 coordinated actions
   👥 Assigned Teams: 5 response teams
   📞 Escalation Contacts: 4 executives
```

## DACP Features Demonstrated

- **3-Stage Multi-Agent Orchestration** - Coordinating specialized security agents
- **Sequential Data Flow** - Threat analysis → Risk assessment → Incident response
- **Conditional Workflow Routing** - Stage 3 triggers based on risk thresholds
- **Multi-Engine Integration** - Claude + OpenAI working seamlessly together
- **Real-time Processing** - Complete security incident response pipeline
- **Structured Data Flow** - Type-safe JSON communication between agents

## Security Agent Patterns

### Threat Analyzer (Claude-Powered)
- **Input**: Security events (failed logins, port scans, data access, etc.)
- **Output**: Threat identification, type classification, severity assessment
- **Behavioral Contract**: Medium conservatism, detailed analysis, strict temperature control
- **Engine**: Claude 3.5 Sonnet for nuanced threat analysis

### Risk Assessor (Claude-Powered)
- **Input**: Threat analysis results + asset context
- **Output**: Risk scores, business impact, immediate actions, mitigation recommendations
- **Behavioral Contract**: Comprehensive evaluation, practical recommendations, safety checks
- **Engine**: Claude 3.5 Sonnet for business-focused risk assessment

### Incident Responder (OpenAI-Powered)
- **Input**: Risk assessment results + threat context
- **Output**: Incident ID, response plans, team assignments, escalation contacts, timelines
- **Behavioral Contract**: Urgency awareness, stakeholder focus, practical coordination
- **Engine**: GPT-4 for structured incident coordination and planning
- **Trigger**: Activated when risk ≥ 7.0 or escalation required

## Integration with Open Agent Stack

This example showcases the complete **OAS + BC + DACP** ecosystem:

- **OAS (Open Agent Spec)** - Declarative agent definitions via YAML
- **BC (Behavioral Contracts)** - Governance and validation using decorators  
- **DACP** - Runtime orchestration and agent communication

## Use Cases

This 3-stage pattern demonstrates production-ready security automation:

- **Complete SOC Automation** - End-to-end security operations center workflows
- **Incident Response Orchestration** - Automated threat → risk → response coordination
- **Multi-Engine Security Analysis** - Leveraging different AI strengths for optimal results
- **Enterprise Risk Management** - Business-aligned threat assessment and escalation
- **Compliance Automation** - Regulatory reporting and audit trail generation
- **Security Team Augmentation** - AI-powered analysis with human oversight integration

## Learn More

- **DACP Documentation** - [dacp repo](https://github.com/aswhitehouse/dacp)
- **Open Agent Stack** - [openagentstack.ai](https://openagentstack.ai)