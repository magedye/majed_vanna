QUICK_START.md
--

# 📄 **Majed Vanna Enterprise Agent — Quick Start Guide**

*(Ready for immediate use in your project root README)*

---

# **🚀 Quick Start — How to Use the Majed Vanna Enterprise Agent**

This is the fastest, simplest way to start working with the Autonomous Agent inside the Majed Vanna Enterprise System.

---

# **1. Start the Agent**

To begin an operational session:

```
AGENT_MODE: OPERATE
```

The Agent will:

* Load the Operating Contract
* Load all project documentation
* Load the Knowledge Base
* Identify the current Phase
* Present a clear list of next-step options

Everything runs in **Simplified Interaction Mode** for an easy user experience.

---

# **2. Start with Full Documentation Sync (Recommended after updates)**

If documentation or ADRs were manually edited:

```
AGENT_MODE: OPERATE
SYNC_DOCUMENTATION: FULL
```

This forces the Agent to re-sync all internal knowledge.

---

# **3. Hold / Stop the Agent**

If you want the Agent to remain idle:

```
AGENT_MODE: HOLD
```

Useful when inspecting or modifying the project manually.

---

# **4. Choosing Actions (Simple & Guided)**

At every decision point, the Agent gives you:

* A numbered list of choices
* A recommended option
* A short explanation
* A pause awaiting your numeric response

Example:

```
1. Proceed to Phase 1.D — Error Handling (Recommended)
2. Proceed to Phase 1.E
3. Pause

Awaiting your selection (1–3).
```

Just reply with the number. That’s it.

---

# **5. Switching Interaction Modes**

Use expert-level explanations:

```
Use full expert mode.
```

Return to default automatically by continuing normally.

---

# **6. Where to Find the Full Documentation**

| Purpose            | Location                                              |
| ------------------ | ----------------------------------------------------- |
| Operating Contract | project_docs/Agent_Operating_Contract.md              |
| Agent Rules        | project_docs/agent_rules.md                           |
| Task Roadmap       | project_docs/tasks.md                                 |
| ADRs               | project_docs/adr/*                                    |
| Knowledge Base     | project_docs/knowledge_base/agent_system_knowledge.md |

---

# **7. Recommended Workflow**

1. Start Agent → `AGENT_MODE: OPERATE`
2. Choose next action from the numbered list
3. Review patch previews
4. Apply / Adjust / Reject (numbers again)
5. Phase completes → Agent pauses
6. Authorize the next Phase
7. Repeat

---

# **8. Important Safety Notes**

* The Agent **must not** override Vanna native functionality
* All changes must be logged and documented
* Human decisions override all automated behavior
* The Agent cannot advance phases without explicit permission

---

# ✔ Done — you are ready to use the system.

---
