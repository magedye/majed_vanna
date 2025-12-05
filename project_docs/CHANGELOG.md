## **Changelog**

### **Unreleased (current)**
- Phase 4 complete (native + docker paths documented)

### **Phase 2**
- Phase 2.B: Added LLM/SQL perf timers, averaged metrics in `/health/perf`; context injection adapter wired to local ChromaDB + LM Studio
- Phase 2.A: Added readiness endpoint and per-IP rate limiting; introduced Oracle SessionPool runner with env-based credentials; completed Phase 1 foundation wrap-up and documentation updates
- Phase 2.C: Added pytest suite (17 passing) covering input/prompt/SQL validation, error handling, agent pipeline stub, sqlite run_sql smoke; added context injection tests

### **Phase 4**
- Phase 4.C: Added native production script `scripts/run_prod.bat` (uvicorn, env setup) and documentation for non-Docker deployment
- Phase 4.B: Nginx reverse proxy with extended timeouts, security headers, WebSocket upgrades, and static offload for `/charts`
- Phase 4.A: Multi-stage Dockerfile (non-root, healthcheck to `/api/health/ready`), docker-compose with app + nginx, volumes for chroma_db and charts

### **Phase 3**
- Phase 3.B: Exposed chart assets via FastAPI StaticFiles (`/charts`) and added `chart_url` metadata while keeping inline ChartComponent rendering
- Phase 3.A: Added SafeVisualizer with sandboxed chart writes to `app/static/charts/<user_hash>/`, filename sanitization, chart JSON persistence, and hash-based user scoping

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

