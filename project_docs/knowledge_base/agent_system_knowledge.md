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
- Database credentials must come from environment variables; no hardcoded DSN/connection defaults are permitted.

#### **8. Operational Notes (Phase 2.A)**
- Oracle uses oracledb SessionPool; credentials via ORACLE_USER/ORACLE_PASSWORD/ORACLE_DSN or DB_ORACLE_DSN.
- Readiness endpoint: `/health/ready` (checks DB connectivity).
- Per-IP rate limiting middleware (defaults: 60 requests/60s) controlled by RATE_LIMIT_MAX_REQUESTS and RATE_LIMIT_WINDOW_SECONDS.

#### **9. Operational Notes (Phase 2.B)**
- LLM middleware logs roundtrip duration and records samples for perf reporting.
- SafeRunSqlTool logs execution duration and records samples.
- `/health/perf` returns recent LLM/SQL timings plus averages (in-memory buffers only).

#### **10. Operational Notes (Phase 2.C)**
- Pytest + pytest-asyncio installed.
- Tests cover input validation, prompt safety, SQL validation, error handling, agent pipeline (stub LLM), and sqlite RunSql smoke.
- Test env defaults to DB_PROVIDER=sqlite for isolation.

#### **11. Operational Notes (Phase 3.A - Visualization Backend)**
- SafeVisualizer wraps VisualizeDataTool and writes chart outputs to `app/static/charts/<user_hash>/` with basename sanitization; filenames and directories are traversal-safe.
- Chart payloads (Plotly JSON) are persisted as `chart_<ts>.json` alongside any generated CSVs; user hash uses SHA256 of `context.user.id` truncated to 16 chars.
- Visualization relies on LocalFileSystem sandbox; LLM roundtrip latency remains high on local hardware (~20–200s).
- Next step (Phase 3.B): expose `app/static/charts` via FastAPI StaticFiles and return renderable Plotly payloads/URLs to the UI.

#### **12. Operational Notes (Phase 4 - Deployment & Runtime)**
- Docker path: multi-stage Dockerfile (non-root, healthcheck to `/api/health/ready`), docker-compose with nginx + app, volumes for `./chroma_db` and `./app/static/charts`.
- Nginx path: reverse proxy on 7770 with increased timeouts (600s, WS 86400s), security headers, WebSocket upgrades, static offload for `/charts`.
- Native path: `scripts/run_prod.bat` starts uvicorn (`app.main:app`) on 0.0.0.0:7777 with workers=2; activate venv if present.

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

