## **ADR‑0003 — Database Engines**

### **Decision**
- **Oracle** is the primary engine.
- **SQLite** included for testing only.

### **Rationale**
Oracle supports enterprise workloads; SQLite accelerates local dev.

### **Impact**
- Maintain two providers