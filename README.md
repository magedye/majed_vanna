# Majed Vanna Enterprise System

Production-grade Vanna-based agent with Oracle primary DB, local LM Studio LLM, and ChromaDB vector memory. Includes semantic context injection, visualization, system governance, and full observability/guardrails.

## Architecture Highlights
- **LLM**: LM Studio (OpenAI-compatible) on host; circuit breaker + timeout/retry guardrails.
- **DB**: Oracle primary (session pool optional) with schema-governed training; SQLite kept for tests.
- **Memory**: ChromaDB persistent store (./chroma_db) pinned to ll-MiniLM-L6-v2 embeddings.
- **Semantic Layer**: Merges all markdown in dbt_integration/ into prompts and published docs.
- **Visualization**: SafeVisualizer sandboxed to pp/static/charts/<user_hash>; served via /charts.
- **Server**: FastAPI + Vanna agent on port 7777; Nginx (docker option) on 7770.

## Key Features
- Input / SQL / Prompt safety layers; structured error envelopes with trace IDs.
- Circuit breakers for LLM & DB; configurable timeouts and retry/backoff.
- Payload cap middleware (MAX_PAYLOAD_SIZE_BYTES, default 1MB).
- Security headers (HSTS, CSP, Referrer-Policy); RBAC for admin ops (dmin@example.com).
- Metrics endpoint /api/metrics; perf history for LLM/SQL; slow-request logging.
- Health endpoints /api/health, /api/health/ready, /api/health/perf (status + trace_id).
- Memory ops API: backup/reset (admin only) plus UI form via MemoryManagementTool.
- Semantic docs: semantic.py build|preview|search, outputs under dbt_integration/docs/.
- RUNBOOK & OPS_SOP for operations and maintenance.

## Run Locally (Native)
1) Install deps: pip install -r requirements.txt
2) Ensure .env set (see Config). Ports are fixed to 7777.
3) Start: scripts\run_prod.bat (kills blocking PID, starts uvicorn on 0.0.0.0:7777).
4) UI: http://localhost:7777

## Run with Docker (optional)
- Build/start: docker compose up -d --build
- App on host port 7777 (or via Nginx 7770 if enabled). Volumes: ./chroma_db, ./app/static/charts.

## Configuration (.env)
- APP_PORT=7777, GATEWAY_PORT=7770
- DB: DB_PROVIDER=oracle, DB_ORACLE_DSN, ORACLE_USER, ORACLE_PASSWORD, ORACLE_SCHEMA, ORACLE_ENABLE_POOL=true, ORACLE_TRAIN_OBJECTS=TABLES,VIEWS, ORACLE_TRAIN_TABLES=ALL
- LLM: LLM_PROVIDER=lmstudio, LM_STUDIO_URL, LM_STUDIO_MODEL
- Guardrails: DB_QUERY_TIMEOUT_MS, DB_MAX_RETRIES, DB_RETRY_BACKOFF_MS, LLM_TIMEOUT_MS, LLM_MAX_RETRIES, LLM_RETRY_BACKOFF_MS, MAX_PAYLOAD_SIZE_BYTES
- Rate limit: RATE_LIMIT_MAX_REQUESTS, RATE_LIMIT_WINDOW_SECONDS

## Admin & Governance
- Admin endpoints: /api/system/backup-memory, /api/system/reset-memory?force=true require anna_email=admin@example.com (cookie/header).
- Audit logs for admin actions include 	race_id and user.
- Security headers applied globally; payloads > limit return 413.

## Training & Memory
- Reset: DELETE /api/system/reset-memory?force=true (admin) then restart.
- Train (Oracle): python scripts/train_local.py (governed by ORACLE_TRAIN_*).
- Vector store readiness visible in /api/health/ready.

## Semantic Docs
- Build unified docs: python semantic.py build
- Outputs: dbt_integration/docs/semantic_docs.md/html/json
- API: /api/semantic/docs, /api/semantic/search?query=...

## Diagnostics
- Health: /api/health/ready
- Metrics: /api/metrics
- Charts: /charts/<user_hash>/<file>

## References
- Operations: RUNBOOK.md
- Maintenance SOP: OPS_SOP.md
- Roadmap: project_docs/tasks.md
- Changes: project_docs/CHANGELOG.md
