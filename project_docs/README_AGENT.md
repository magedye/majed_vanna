```
README_AGENT.md
```

This version is polished, production-ready, and aligned with your full documentation system, the Agent Operating Contract, and all rules (07–09).

---

# 📄 **FINAL README — How to Start and Operate the Agent**

*(Ready to paste directly into your project)*

---

# **Majed Vanna Enterprise Agent — User Operations Guide**

This document explains how to start, interact with, and control the Autonomous Agent operating inside the Majed Vanna Enterprise System.
It is written for project maintainers, developers, and system operators.

---

# **1. Purpose of the Agent**

The Agent automates development tasks, code generation, patch preparation, documentation updates, and system stabilization in a strictly controlled, phase-based execution model.

It is governed entirely by:

* **Agent Operating Contract**
* **AI Agent Behavior Rules**
* **ADR architectural decisions**
* **Vanna compliance requirements**
* **Simplified Interaction Mode (default)**

---

# **2. Starting a New Session**

To begin a new session with the Agent, use the following command:

```
AGENT_MODE: OPERATE
```

This instructs the Agent to:

* Load the full Operating Contract
* Load all documentation under project_docs/*
* Load the complete Knowledge Base
* Sync ADRs and architectural constraints
* Enter the authorized Phase’s autonomous execution mode
* Activate Simplified Interaction Mode

The Agent will then detect the current Phase and present the next recommended action as a numbered choice list.

---

# **3. Starting With Full Documentation Sync**

If you want the Agent to re-load all documents from scratch (clean state):

```
AGENT_MODE: OPERATE
SYNC_DOCUMENTATION: FULL
```

Use this when:

* Documentation was updated manually
* New ADRs were added
* Knowledge Base was modified
* A new feature or architectural decision was introduced

---

# **4. Holding the Agent (No Execution)**

If you want the Agent to remain idle and not take any action:

```
AGENT_MODE: HOLD
```

In HOLD mode, the Agent:

* Loads nothing
* Executes nothing
* Waits for further instruction

---

# **5. Interaction Model (Simplified Mode)**

The Agent always provides:

* Short, clear responses
* Numbered action choices
* A recommended option
* A rationale for the recommendation
* A pause while waiting for your numeric selection

Example:

```
Phase 1.C complete. Choose:

1. Proceed to Phase 1.D (Recommended)
   Why: Error handling should precede secrets management.

2. Proceed to Phase 1.E
   Why: Only appropriate after 1.D.

3. Pause

Awaiting your selection (1–3).
```

To switch briefly to expert mode:

```
Use full expert mode.
```

To return to Simplified Interaction Mode, simply continue — it is the default.

---

# **6. Ending a Session**

There is no shutdown command required.
The Agent simply pauses after completing a Phase or receiving:

```
AGENT_MODE: HOLD
```

---

# **7. Operational Safety Rules (Summary)**

The Agent must:

* Remain documentation-driven
* Respect Vanna’s architectural boundaries
* Never override native Vanna functionality
* Update documentation after code modifications
* Log all execution steps into `audit.log`
* Pause between phases and wait for approval
* Follow Rules 07-09 (interaction protocol)

---

# **8. Recommended Workflow**

1. Start a session:

```
AGENT_MODE: OPERATE
```

2. Review recommended action
3. Choose a number (1–3)
4. Agent drafts patch → You review → You choose Apply/Adjust/Reject
5. Repeat until phase complete
6. Agent pauses
7. You authorize next phase

---

# **9. Where to Find Key Documents**

| Purpose                       | Location                                                |
| ----------------------------- | ------------------------------------------------------- |
| Operating Contract            | `project_docs/Agent_Operating_Contract.md`              |
| Agent Behavior Rules          | `project_docs/agent_rules.md`                           |
| Task Roadmap                  | `project_docs/tasks.md`                                 |
| Knowledge Base                | `project_docs/knowledge_base/agent_system_knowledge.md` |
| Architectural Decisions (ADR) | `project_docs/adr/*`                                    |
| Notes & Ideas                 | `project_docs/notes_and_ideas.md`                       |
| Architecture                  | `project_docs/architecture.md`                          |

---

# **10. Support**

For updates, amendments, or issues, submit a new ADR:

```
project_docs/adr/ADR-xxxx-agent-contract-amendment.md
```

The human system owner is the final authority over all Agent behavior.

---

# ✔ End of User Operations Guide

---

