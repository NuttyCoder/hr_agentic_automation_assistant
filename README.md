# HR Agentic Automation Assistant

An AI-powered HR automation platform demonstrating how modern HR organizations can leverage large language models, agentic decision-making, Python microservices, and RPA-style automation to streamline employee support.

This portfolio project simulates end-to-end enterprise HR automation: from conversational intent parsing to multi-step orchestrations that call microservices and RPA bots while enforcing governance, PII masking, and auditability.

---

## Table of contents
- [Project Goals](#project-goals)
- [Core Features](#core-features)
- [Example Workflows](#example-workflows)
  - [PTO Request](#pto-request)
  - [Update Address (Multi-step)](#update-address-multi-step-agentic-flow)
- [System Architecture](#system-architecture)
- [Tech Stack](#tech-stack)
- [Repository Structure](#repository-structure)
- [Quickstart](#quickstart)
- [Included Documentation](#included-documentation)
- [Demo Script (For Recruiters & Hiring Managers)](#demo-script-for-recruiters--hiring-managers)
- [Why This Project Matters](#why-this-project-matters)
- [Contributing](#contributing)
- [License](#license)

---

## Project Goals
This project was built to:
- Demonstrate mastery of LLM-driven conversational interfaces
- Show how to design agentic workflows that make autonomous decisions
- Integrate with mock HR systems (ServiceNow-like, SuccessFactors-like)
- Simulate RPA bots for legacy system automation
- Implement Python microservices for HR data operations
- Showcase data governance, PII masking, and audit logging
- Provide a realistic example of enterprise HR automation

## Core Features
flowchart TD
    %% Conversation Layer
    subgraph ConversationLayer["Conversation Layer"]
        Webhook[Webhook]:::conv
        Intent[Intent Classifier]:::conv
        Agentic[HR Orchestrator Agent]:::conv
    end

    %% Orchestration Layer
    subgraph OrchestrationLayer["Orchestration Layer"]
        Runner[Workflow Runner (YAML)]:::orch
        Context[Orchestration Context]:::orch
        Registry[Tools Registry]:::orch
    end

    %% Services Layer
    subgraph ServicesLayer["Services Layer"]
        Profile[HR Profile Service]:::serv
        PTO[PTO Service]:::serv
        Ticket[Ticketing Service]:::serv
        Benefits[Benefits Service]:::serv
        Policy[Policy Service]:::serv
        Notify[Notification Service]:::serv
    end

    %% Adapters Layer
    subgraph AdaptersLayer["Adapters Layer"]
        SN[ServiceNow Adapter]:::adapt
        SF[SuccessFactors Adapter]:::adapt
        Email[Email Client]:::adapt
        Slack[Slack Client]:::adapt
    end

    %% RPA Layer
    subgraph RPALayer["RPA Layer"]
        RPAEngine[RPA Engine]:::rpa
        AddressBot[Address Update Bot]:::rpa
        PayrollBot[Payroll Investigation Bot]:::rpa
    end

    %% Governance Layer
    subgraph GovernanceLayer["Governance Layer"]
        PII[PII Masking]:::gov
        PolicyEng[Policy Engine]:::gov
        Audit[Audit Logger]:::gov
        Roles[Role Permissions]:::gov
    end

    %% Connections
    Webhook --> Intent --> Agentic
    Agentic --> Runner --> Registry
    Runner --> Context

    Registry --> Profile
    Registry --> PTO
    Registry --> Ticket
    Registry --> Benefits
    Registry --> Policy
    Registry --> Notify

    Registry --> SN
    Registry --> SF
    Registry --> Email
    Registry --> Slack

    Registry --> RPAEngine
    RPAEngine --> AddressBot
    RPAEngine --> PayrollBot

    Agentic --> GovernanceLayer

    %% Styles
    classDef conv fill=#1f77b4,stroke=#ffffff,color=#ffffff;
    classDef orch fill=#2ca02c,stroke=#ffffff,color=#ffffff;
    classDef serv fill=#9467bd,stroke=#ffffff,color=#ffffff;
    classDef adapt fill=#ff7f0e,stroke=#ffffff,color=#ffffff;
    classDef rpa fill=#17becf,stroke=#ffffff,color=#ffffff;
    classDef gov fill=#d62728,stroke=#ffffff,color=#ffffff;
1. Conversational AI Interface
   - Natural language understanding
   - Intent classification
   - Entity extraction
   - Clarification questions
   - JSON-structured responses for downstream automation

2. Agentic Workflow Orchestrator
   - Multi-step workflow execution
   - Tool selection and routing
   - Error handling + retry logic
   - Escalation to HR when automation fails
   - Config-driven behavior for HR admins

3. Python Automation Microservices
   - FastAPI-based service layer
   - Endpoints for PTO balance lookup, address updates, ticket creation
   - SQLite-backed HR database
   - Role-based access control and audit logging

4. RPA Simulation Layer
   - Python-based “bots” that mimic RPA behavior
   - Simulated login, screen scraping, and delayed execution
   - Bot action logging and outcome tracking

5. HR System Integrations (Mocked)
   - ServiceNow-style ticketing
   - SuccessFactors-like employee profile system
   - Realistic REST APIs and data models

6. Governance & Security
   - PII masking in logs
   - Role-based access (Employee vs HR Admin)
   - Configurable automation rules
   - Full audit trail of actions

## Example Workflows
sequenceDiagram
    participant U as User
    participant W as Webhook (Moveworks-style)
    participant A as HR Orchestrator Agent
    participant R as Workflow Runner
    participant S as Services (HR Profile, PTO, Ticketing)

    U->>W: Submit PTO request (dates, days_requested)
    W->>A: Forward intent + entities
    A->>R: Load workflow (request_time_off.yaml)

    R->>S: get_employee_profile
    S-->>R: Employee profile data

    R->>S: get_pto_balance
    S-->>R: PTO balance result

    alt Enough PTO balance
        R->>S: create_pto_request
        S-->>R: PTO request confirmation
        R-->>A: Final output (approved PTO)
    else Insufficient PTO balance
        R->>S: create_ticket
        S-->>R: Ticket ID + escalation
        R-->>A: Final output (escalated to HR)
    end

    A-->>W: Return response
    W-->>U: PTO request result (approved or escalated)
### PTO Request
User: “Can you tell me how much PTO I have left?”

Flow:
1. Conversational AI identifies intent
2. Orchestrator selects PTO workflow
3. Microservice queries PTO balance
4. Orchestrator formats response
5. Chat layer returns answer
6. Audit log records the interaction

Result: Automated, traceable response with auditability.

### Update Address (Multi-step Agentic Flow)
User: “I moved — update my address to 123 Main St.”

Flow:
1. LLM extracts intent and entities
2. Orchestrator validates address format
3. Calls HR microservice to update the DB
4. Calls RPA bot to update a legacy system
5. Confirms success to user
6. Logs user ID, systems touched, masked PII, timestamp, and outcome

Result: Realistic simulation of API-driven and RPA-driven enterprise automation.

## System Architecture
High-level components:
- Chat / LLM layer for user interaction and intent parsing
- Agentic orchestrator to sequence tools and workflows
- FastAPI microservices for HR operations and data
- RPA simulation layer for legacy system interactions
- SQLite for demo data persistence and audit logs
- Admin UI for rules, logs, and governance

(See /docs for diagrams and detailed component maps)

## Tech Stack
- Backend: Python, FastAPI, SQLite
- Communication: HTTPX / requests
- AI Layer: LLM (OpenAI-style or local models), prompt engineering
- Orchestration: LangChain-style agent, tool abstractions
- RPA Simulation: Python scripts with logging and delays
- Frontend: Minimal chat UI (HTML/JS or Streamlit), HR admin dashboard

## Repository Structure
- /chatbot/               — Conversational AI layer
- /orchestrator/          — Agentic workflow engine
- /services/hr_system/    — HR microservices (PTO, profile, tickets)
- /services/rpa_sim/      — RPA bot simulation
- /admin/                 — HR admin console
- /docs/                  — Architecture diagrams, specs, case study
- README.md               — This file

## Quickstart
1. Clone repo:
   git clone https://github.com/NuttyCoder/hr_agentic_automation_assistant.git
2. Create virtualenv and install:
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
3. Start services (example):
   - Start FastAPI microservices: `uvicorn services.hr_system.main:app --reload`
   - Start conversational UI: open /chatbot or run streamlit if provided
4. Seed demo data (if a seed script exists): `python scripts/seed_db.py`
5. Use the chat UI to run sample workflows from the Demo Script.

(Adjust commands according to the repository’s run scripts or Docker setup in /docs)

## Included Documentation
- System architecture diagram
- Data flow diagrams
- Sequence diagrams for each workflow
- Security & governance model
- Component interaction map
- Full case study and demo script

## Demo Script (For Recruiters & Hiring Managers)
1. Start the chat UI and ask: “What’s my PTO balance?”
2. Run a multi-step workflow: “Request PTO from Feb 10–12.”
   - Show decision-making and ticket creation
3. Update address to demonstrate RPA bot simulation
4. Open the HR admin console to show masked PII, logs, and automation rules
5. Trigger a failure to show graceful fallback and escalation

## Why This Project Matters
Demonstrates practical application of:
- LLM integration in enterprise workflows
- Agentic decision-making and tool use
- API-driven automation plus RPA orchestration
- Data governance and security in automated systems

## Contributing
Contributions are welcome. Please:
1. Open an issue describing the change or feature.
2. Fork the repo and create a branch for your patch.
3. Submit a pull request with tests/docs where relevant.

## License
Specify your license here (e.g., MIT). If none is present, add a LICENSE file.
