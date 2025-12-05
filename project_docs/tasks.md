Roadmap & Operational Tasks

Project: Majed Vanna Enterprise System
Maintained by: Autonomous Agent (under contract)
Last Updated: {auto-update by agent}

Legend
- Done
- In Progress
- Pending
- Blocked / Requires Human Approval

------------------------------------------------------------
Phase 1 — Core Stabilization (Done 5/5)

1.A Input Safety Layer — Done
- Message sanitization, metadata validation, ID rules, FastAPI middleware, SafeChatHandler

1.B SQL Safety Layer — Done
- Single-statement enforcement, destructive keyword blocking, comment/tautology filters, SafeRunSqlTool wrapper

1.C Prompt Safety Layer — Done
- Regex/rule filters, meta-instruction blocks, control-char stripping

1.D Unified Error Handling — Done
- API-level handlers, user-friendly error responses, internal logging hooks

1.E Secrets & Environment Hardening — Done
- Secrets moved to .env, hardcoded DSNs removed, env validation added

------------------------------------------------------------
Phase 2 — Stabilization II (Done 3/3)

2.A Operational Stabilization — Done
- Oracle SessionPool, SQLite testing stability, readiness endpoint, lightweight rate limiting

2.B Performance Stabilization — Done
- LLM latency metrics, DB roundtrip metrics, /health/perf averages, context injection adapter (ChromaDB + LM Studio)

2.C Test Coverage — Done
- 17 passing tests (input/prompt/SQL validation, error handling, agent pipeline stub, sqlite run_sql)
- pytest + pytest-asyncio installed; context injection tests added; baseline coverage achieved

------------------------------------------------------------
Phase 3 — UI / UX Enhancements (Done 2/2)

3.A Secure Visualization Backend — Done
- SafeVisualizer sandboxed to app/static/charts/<user_hash>, filename sanitization, chart JSON persistence

3.B Frontend Visualization Integration — Done
- Charts exposed via FastAPI StaticFiles at /charts, chart_url metadata returned, inline ChartComponent preserved

------------------------------------------------------------
Phase 4 — Deployment & Runtime (Done 3/3)

4.A Containerization — Done
- Multi-stage Dockerfile (non-root, healthcheck, uvicorn CMD), docker-compose with nginx/app, volumes for chroma_db and charts

4.B Nginx Layer — Done
- Reverse proxy with increased timeouts, security headers, WebSocket upgrades, static offload for /charts

4.C Service Installation / Native Finalization — Done
- Added scripts/run_prod.bat for native uvicorn startup (no Docker required)
- Documented Docker (Method A) and Native (Method B) deployment paths

------------------------------------------------------------
Cross-Phase Tasks (Always Active) — Ongoing
- Maintain agent_system_knowledge.md
- Update ADRs when decisions occur
- Log behavioral changes
- Enforce Agent Operating Contract, agent_rules.md, and Vanna compliance

------------------------------------------------------------
Summary Dashboard
- Phase 1: 5/5 completed
- Phase 2: 3/3 completed
-> Phase 3: 2/2 completed
- Phase 4: 3/3 completed
- Cross-phase operations: active

