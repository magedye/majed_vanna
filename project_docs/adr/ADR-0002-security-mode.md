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