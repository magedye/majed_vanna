
```
project_docs/objectives.md
```

---

# **Project Objectives & Metrics (Enterprise Edition)**

## **1. Primary System Objectives**

### **1.1 Deliver Secure LLM-Driven Data Intelligence**

* Natural-language input → validated SQL → trusted execution.
* Full compliance with:

  * Input Safety Layer
  * Prompt Safety Layer
  * SQL Safety Layer
* Prevent unsafe model outputs through multi-layer guardrails.

### **1.2 Ensure Absolutely Safe SQL Execution**

* Enforce single-statement SQL.
* Validate query structure before runtime.
* Block destructive or unsupported SQL paths.
* Guarantee zero direct execution of unvalidated SQL.

### **1.3 Provide Enterprise-Grade Auditability & Traceability**

* Comprehensive execution logging (audit.log).
* Phase-based development traceability.
* ADR-driven architectural history and decision lifecycle.
* Full visibility into tool execution and agent actions.

### **1.4 Support Oracle as a First-Class Backend**

* Robust and stable connection pooling.
* Safe connection lifecycle management.
* Consistent, high-quality metadata extraction.
* Optional SQLite support for testing and offline development.

### **1.5 Enable a Scalable Semantic Layer Architecture**

* Modular metadata providers (Oracle, SQLite, dbt, JSON).
* Future-ready foundation for automated semantic enrichment.
* Extensible model for lineage, vocabulary, metrics, and intents.

### **1.6 Guarantee Predictable Agent Behavior**

* Full alignment with the Agent Operating Contract.
* Deterministic decision-making governed by documented rules.
* Simplified Interaction Mode as default.
* Zero unauthorized execution outside approved phases.

---

## **2. Success Metrics (KPIs)**

### **2.1 Security KPIs**

* **0 critical vulnerabilities** across all safety layers.
* **100% of SQL statements validated** before execution.
* **< 100 ms** additional latency introduced by validation layers.

### **2.2 LLM Cost & Efficiency KPIs**

* **≥ 30% reduction** in LLM token usage due to dual-output pattern.
* **< 5% unexpected LLM clarification requests**, indicating effective prompt filtering.

### **2.3 Backend Performance KPIs**

* **99.9% stability** of Oracle connection pool under load.
* **< 150 ms (p95)** SQL execution latency for standard workloads.

### **2.4 UI Performance KPIs**

* **< 200 ms** interaction latency for data loads, lineage views, and table rendering.
* UI component lifecycle optimized to **≤ 2 re-renders** per interaction.

### **2.5 Agent Behavior KPIs**

* **0 unauthorized phase transitions**.
* **100% compliance** with:

  * Agent Operating Contract
  * Safety Layers
  * Architecture Constraints
* **All patches logged** in:

  * audit.log
  * project_docs/tasks.md

---

## **3. Operational SLAs**

| SLA Metric                    | Target                            |
| ----------------------------- | --------------------------------- |
| System uptime                 | **99.5%**                         |
| Agent (non-LLM) response time | **< 1 second**                    |
| Semantic model regeneration   | **< 3 seconds** for ≤ 200 tables  |
| Oracle metadata refresh       | **< 2 seconds** under normal load |

---

## **4. Definition of “Project Success”**

The project is considered successful when all of the following are achieved:

1. **End-to-end user experience:**
   Users ask natural questions → system generates safe SQL → executes securely → returns interactive results.

2. **Full implementation of safety layers:**

   * Input validation
   * Prompt filtering
   * SQL validation
     All validated and operational.

3. **Enterprise-grade Oracle backend stability:**
   The system reliably handles production-level Oracle workloads with minimal latency.

4. **Contract-governed agent operation:**
   The agent behaves deterministically, within documented rules, pausing at phase boundaries.

5. **Documentation completeness and consistency:**
   project_docs/* remains updated, synchronized, and aligned with actual system behavior.

---
