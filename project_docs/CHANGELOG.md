## **Changelog**

### **Unreleased (current)**
- Phase 2.B: Added LLM/SQL perf timers, averaged metrics in `/health/perf`
- Phase 2.A: Added readiness endpoint and per-IP rate limiting
- Phase 2.A: Introduced Oracle SessionPool runner with env-based credentials
- Phase 2.A: Completed Phase 1 foundation wrap-up and documentation updates
- Phase 2.C: Added pytest suite (17 passing) covering input/prompt/SQL validation, error handling, agent pipeline stub, sqlite run_sql smoke

### **Phase 1.E**
- Removed hardcoded DSN defaults; enforced env-only secrets

### **Phase 1.D**
- Centralized FastAPI exception handling with safe responses

### **Phase 1.C**
- Prompt Safety Filter for meta-instruction blocking

### **Phase 1.B**
- SQL Safety Layer with single-statement and destructive keyword blocking

### **Phase 1.A**
- Request Input Validation Middleware and SafeChatHandler
