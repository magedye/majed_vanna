# Enterprise Documentation Package for Majed Vanna Project

This document contains **all project documentation files** requested, in final production‑grade form. Each section represents a file that should be saved into the project under `project_docs/` (or its subdirectories).

You may extract each section into its intended file path.

---

# FILE 1: project_docs/overview.md

## **Majed Vanna Project — Overview**

### **Purpose**
The Majed Vanna Project provides a **secure, user‑aware, enterprise‑grade LLM analytical agent** built on Vanna’s core architecture and extended with modular components for metadata intelligence, SQL reasoning, controlled execution, and interactive UI rendering.

### **Primary Objectives**
- Deliver natural‑language analytical capabilities safely.
- Execute SQL through strictly protected pipelines.
- Provide rich UX elements including tables, charts, lineage views.
- Maintain strict permission enforcement and session isolation.
- Support both **Oracle (primary)** and **SQLite (testing)** as data sources.
- Integrate cleanly with LM‑Studio as default LLM provider.

### **High-Level Features**
- User‑aware agent with per‑user security and quota controls.
- Stateful UI supporting interactive artifacts.
- Automated metadata extraction and semantic expansion (future phase).
- Fully auditable execution with logging and stable API surface.

---

# FILE 2: project_docs/architecture.md

## **System Architecture — Majed Vanna Project**

### **Layers**

#### 1. **UI Layer**
- `<vanna-chat>` web component
- React-based admin UI (optional future)
- Delivered via FastAPI static hosting

#### 2. **API Layer (FastAPI)**
- Chat endpoints
- Health & status
- Metadata endpoints
- Middleware for identity, quota, input validation

#### 3. **Agent Layer**
- Workflow manager
- Security filters (Phase 1)
- Memory/session manager
- Tool selector

#### 4. **Tools Layer**
- SQL Executor
- Metadata Providers (Oracle, SQLite, dbt, DataHub)
- File/OS/API utilities
- Visualization/Artifact generator

#### 5. **LLM Layer**
- LM Studio via OpenAI-compatible REST
- Summary transformations
- Prompt safety filters

### **Data Flow Summary**
```
User → FastAPI → Security → Workflow → Tool → LLM (summary) → UI Artifact → Frontend
```

### **Key Architectural Guarantees**
- Zero breaking changes during phased rollout.
- Strict module-to-module boundaries.
- Security-first pipeline.

---

# FILE 3: project_docs/adr/ADR-0001-initial-architecture.md

## **ADR‑0001 — Initial System Architecture**

### **Decision**
Adopt a modular, layered architecture with strict boundaries between UI, API, Agent, Tools, and LLM layers.

### **Rationale**
- Maintainability
- Security isolation
- Replaceability of components
- Enterprise readiness

### **Consequences**
- Clear separation of concerns
- Faster future enhancements

---

# FILE 4: project_docs/adr/ADR-0002-security-mode.md

## **ADR‑0002 — Security Mode Design**

### **Decision**
Implement two modes:
- `ENV_SECURITY_MODE=off` → basic sanitization only
- `ENV_SECURITY_MODE=on` → advanced SQL, prompt, and permission guards

### **Reasoning**
Allows flexible development while enabling production‑grade lockdown.

### **Impact**
- Feature flags at runtime
- Avoid unnecessary complexity in early phases

---

# FILE 5: project_docs/adr/ADR-0003-database-choice.md

## **ADR‑0003 — Database Engines**

### **Decision**
- **Oracle** is the primary engine.
- **SQLite** included for testing only.

### **Rationale**
Oracle supports enterprise workloads; SQLite accelerates local dev.

### **Impact**
- Maintain two providers

---

# FILE 6: project_docs/CHANGELOG.md

## **Changelog**

### **Unreleased (current)**
- Added enterprise documentation package
- Enabled Phase 1.A input validation design
- Defined architecture + ADR framework

### **Phase 1.A**
- Added Request Input Validation Middleware
- Added SafeChatHandler

---

# FILE 7: project_docs/tasks.md

## **Roadmap & Tasks**

### **Phase 1 — Stabilization**
#### A. Input Safety Layer *(in progress)*
- Validate incoming payloads
- Strip unsafe characters
- Enforce ID & metadata patterns

#### B. SQL Safety Layer *(pending)*
- Parameterized SQL enforcement
- Query‑shape validator

#### C. Prompt Safety Layer *(pending)*
- Regex filters
- Rule-based content blocks

#### D. Error Handling *(pending)*
- Unified exception layer

#### E. Secrets Management *(pending)*
- Move all secrets to `.env`

### **Phase 2 — Stabilization II**
- Oracle pooling
- SQLite refinement
- Health probes

### **Phase 3 — UI Enhancements**
- Stateful components
- Visualization modules

### **Phase 4 — Deployment**
- Docker
- Nginx
- Service integration

---

# FILE 8: project_docs/agent_rules.md

## **AI Agent Behavior Rules**

### **What the Agent MUST Do**
- Respect the Implementation Directive
- Execute only within the authorized phase
- Propose patches before applying them
- Keep all changes localized to scope
- Request clarification when encountering ambiguity

### **What the Agent MUST NEVER Do**
- Modify Vanna core functionality
- Change project architecture
- Add new subsystems without ADR
- Enable advanced security mode without approval
- Alter LLM provider logic

### **Guidance**
The agent operates in **gated phases** and must await approval between each.

---

# FILE 9: project_docs/components_reference.md

## **Components Reference**

### **1. Agent Layer**
- `builder.py` — agent construction
- `workflow.py` — message → tool routing
- `security.py` — permission validation
- `memory.py` — session isolation

### **2. Tools Layer**
- `db.py` — SQL executor
- `tools.py` — utility tools
- `metadata providers` — Oracle, SQLite, DataHub, dbt

### **3. API Layer**
- `router.py` — all routes
- `metadata.py` — schema extraction interface

### **4. UI Layer**
- `static/index.html`
- `vanna-components.js`

### **5. Utility Layer**
- `logger.py` — structured logging
- `helpers.py` — request helpers

---

# FILE 10: project_docs/objectives.md

## **Project Objectives & Metrics**

### **Primary Goals**
1. Provide secure LLM-driven data analysis
2. Guarantee safe SQL execution
3. Deliver enterprise-grade auditability
4. Support Oracle as a first-class backend
5. Maintain extensibility for semantic layers

### **Success Metrics**
- Zero critical security defects in input/SQL layers
- Stable Oracle connections under load
- Interactive UI latency < 200ms
- ≤ 30% LLM token waste reduction via dual-output pattern

---

# FILE 11: project_docs/notes_and_ideas.md

## **Notes, Ideas & Future Considerations**

### **General Notes**
- Semantic model integration should remain optional.
- Future versions may integrate lineage graph rendering.

### **Improvements**
- Add advanced SQL AST validator
- Create agent pre-check pipeline for dangerous queries

### **Technical Considerations**
- Evaluate replacing local LM Studio with on-prem OpenAI-compatible runtime

---

# FILE 12: project_docs/knowledge_base/agent_system_knowledge.md

## **Agent System Knowledge Base**

### **Purpose**
This document defines what the AI Agent must *know* about the project to operate safely and intelligently.

### **Key Knowledge Domains**

#### **1. Project Mission**
Enable secure, enterprise-grade natural language analytics.

#### **2. Hard Constraints**
- Oracle is the primary database.
- LM Studio is the only default LLM.
- Do not modify Vanna core pipeline.
- All changes must follow the Implementation Directive.

#### **3. Execution Phases**
The agent must always operate inside the currently authorized phase.

#### **4. File-Level Responsibilities**
Every module has a strict boundary; unauthorized cross-module edits are prohibited.

#### **5. Security Expectations**
The agent must:
- sanitize input
- validate IDs
- prevent injection
- never transform execution context

#### **6. Patch Workflow**
1. Detect affected files
2. Propose diff
3. Await approval
4. Apply patch

### **7. Knowledge of Existing Constraints**
- Avoid creating new architectural patterns
- Never auto-enable enhanced security mode
- Avoid adding LLM providers
- Avoid semantic layer work unless explicitly authorized

---

# END OF DOCUMENT PACKAGE


