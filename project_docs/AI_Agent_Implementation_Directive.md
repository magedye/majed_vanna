```
project_docs/AI_Agent_Implementation_Directive.md
```

This is the **final authoritative version** that your AI Agent MUST follow.
You may copy & paste it directly into the file without modification.

---

# 🚀 **AI AGENT IMPLEMENTATION DIRECTIVE — MAJED VANNA PROJECT**

### **Final Official Directive (Security Mode, Oracle Priority, Full Vanna Features)**

### **Version: 1.0 — December 2025**

---

## **1. Overview**

This directive defines the *only* authorized actions the AI Agent may perform inside the Majed Vanna project.
The purpose is to stabilize the system, enforce core security, prepare for later enhancements, and maintain full compatibility with the Vanna AI framework.

The agent MUST follow this directive strictly and may NOT act outside of these boundaries.

---

# **2. Project Database Rules**

### ✔ **Primary Database (MANDATORY): Oracle**

The system MUST be optimized around Oracle as the main production database.

### ✔ **Secondary Database (Optional for Local Testing Only): SQLite**

SQLite MAY be used for:

* Local development
* Unit tests
* Feature introspection

### ✖ Forbidden:

* Adding or maintaining any additional database providers
* Introducing PostgreSQL, MySQL, MSSQL, or others

---

# **3. LLM Provider Rules**

### ✔ **Default LLM Provider: LM Studio (OpenAI-compatible REST mode)**

The current integration MUST remain as-is.

### ✔ Allowed:

* OpenAI-compatible models via LM Studio REST
* Zero changes to API schema

### ✖ Forbidden:

* Introducing additional LLM providers
* Refactoring LLM architecture
* Modifying model-selection logic

---

# **4. Security Mode System**

You MUST implement and respect this environment variable:

```
ENV_SECURITY_MODE=on   # Enable enhanced security
ENV_SECURITY_MODE=off  # Default mode (basic security only)
```

---

# **5. Security Requirements**

## **5.1 Basic Security (Always Active)**

These MUST be enforced regardless of security mode:

### ✔ SQL Injection Basic Protection

* Parameterized queries only
* No multi-statements
* No execution of DROP/DELETE/ALTER unless explicitly whitelisted

### ✔ Basic Prompt Injection Protection

* Filter system-level overrides
* Block role-specification attempts
* Block query-shape modification prompts

### ✔ Error Handling

* Never expose stack traces to the user
* All errors must map to safe generic messages
* Internal details go to logs only

### ✔ Secrets Management

* No secrets in code
* All secrets MUST come from `.env`

### ✔ Logging

* Logging MUST NOT reveal sensitive fields

---

## **5.2 Enhanced Security (Active Only When ENV_SECURITY_MODE=on)**

When the variable is “on”, the agent MUST activate:

### 🔒 Advanced SQL Guard

* AST parsing
* Strict query-shape validation
* Reject destructive or suspicious statements

### 🔒 Advanced Prompt Guard

* NLP-based detection of adversarial intent
* Context isolation
* Output validation after LLM generation

### 🔒 Enhanced Logging

* Structured logs (JSON)
* Correlation IDs
* Sensitive field masking

### 🔒 Enhanced DB Safety

* Optional read-only enforcement
* Strict fetch limits
* Suspicious query detection

### ✔ Rule:

**These features MUST NOT activate unless explicitly triggered by the environment variable.**

---

# **6. Vanna Feature Support Rules**

The agent MUST preserve **all native Vanna features** without modification or omission:

### ✔ Mandatory Supported Features

* `ask()`
* `explain()`
* `summarize_results()`
* `generate_followup_questions()`
* `get_results()`
* `train(ddl, documentation, sql, df)`
* SQL validation
* Query execution
* Vector store retrieval
* Visualization features
* All mixins (vector store + LLM + DB provider)

### ✖ Forbidden:

* Removing or downgrading Vanna functionality
* Wrapping or replacing core Vanna internals
* Altering Vanna’s training pipeline

---

# **7. UI Rules**

### ✔ Allowed:

* Use ONLY built-in Vanna UI components
* Serve default Vanna interface as-is

### ✖ Forbidden:

* Designing new UI screens
* Extending the UI
* Adding frontend frameworks
* Modifying JavaScript components beyond bug fixes

---

# **8. Deployment Rules**

### ✔ Allowed Now:

* Running locally via:

  ```
  uvicorn app.main:app --reload
  ```
* Testing endpoints
* Verifying Oracle/SQLite integrations

### ✖ Forbidden Now:

* Docker deployment
* Nginx reverse proxy
* Linux/Windows service installation
* Production server setup

### ✔ Allowed Later (after stabilization):

* Docker & Nginx
* Windows/Linux services

---

# **9. Phase 1 Tasks (Authorized for Immediate Execution)**

The agent MUST execute the following tasks in order, and MUST NOT proceed until each step is completed and stable.

### **Phase 1.A — Input Safety Layer**

* Add input validators
* Enforce schema constraints
* Sanitize natural language queries

### **Phase 1.B — SQL Safety Layer**

* Implement parameterized queries
* Add safety checks
* Introduce SQL validation guard

### **Phase 1.C — Prompt Safety Layer**

* Add regex-based & rule-based filters
* Block meta-instruction patterns

### **Phase 1.D — Error Handling**

* Unified exception layer
* User-safe responses
* Internal logging for debugging

### **Phase 1.E — Secrets & Environment**

* Move ALL sensitive values to `.env`
* Audit repository to ensure zero plaintext secrets

---

# **10. Phase 2 Tasks (Authorized After Phase 1 Completion)**

### **Phase 2.A — Operational Stabilization**

* Fix connection pooling for Oracle
* Stabilize SQLite testing mode
* Add health checks
* Add request rate limiting

### **Phase 2.B — Performance Stabilization**

* Validate LLM latency path
* Validate DB roundtrip performance

### **Phase 2.C — Test Coverage**

* Achieve at least 20–30% unit test coverage
* Ensure ask() pipeline is fully tested
* Add integration tests for Oracle and SQLite

---

# **11. Forbidden Actions (Critical Section)**

The AI Agent MUST NOT:

* Add or begin implementing the semantic layer
* Modify the semantic_model.yaml or metadata folder
* Add cross-database abstraction logic
* Add new LLM providers
* Activate Docker or Nginx
* Introduce architecture refactoring
* Change folder structure
* Remove any existing file unless explicitly instructed
* Implement advanced RBAC or authentication
* Add caching layers or complex middlewares

If uncertain, the agent MUST stop and request clarification.

---

# **12. Completion Criteria Before Any Next Phase**

The agent MUST NOT proceed to any next stage unless ALL of the following are true:

### ✔ Security

* No SQL injection vulnerabilities
* No prompt injection vulnerabilities
* Error messages fully sanitized

### ✔ Stability

* Oracle workflow stable
* SQLite testing stable
* No runtime crashes
* ask(), explain(), summarize_results(), generate_followup_questions() all operational

### ✔ Testing

* Minimum test coverage reached
* All tests pass reliably on repeated runs

### ✔ Configuration

* ENV_SECURITY_MODE toggle fully functional

---

# **13. End of Directive**

Any action outside the scope of this directive is strictly prohibited unless the human project owner manually updates this file.

The agent MUST read and respect this directive before making any change.

---
