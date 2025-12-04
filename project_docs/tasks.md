Roadmap & Operational Tasks

Project: Majed Vanna Enterprise System
Maintained by: Autonomous Agent (under contract)
Last Updated: {auto-update by agent}

Legend
- ✅ Done
- 🚧 In Progress
- ⏳ Pending
- ⛔ Blocked / Requires Human Approval

------------------------------------------------------------
Phase 1 — Core Stabilization (✅ 5/5 complete)

1.A Input Safety Layer — ✅ Done
- Message sanitization
- Metadata validation
- ID rules
- FastAPI middleware integration
- SafeChatHandler activation

1.B SQL Safety Layer — ✅ Done
- Single-statement enforcement
- Block destructive keywords
- Comment + tautology filters
- SafeRunSqlTool wrapper

1.C Prompt Safety Layer — ✅ Done
- Regex/rule filters
- Meta-instruction blocks
- Control-char stripping

1.D Unified Error Handling — ✅ Done
- API-level handlers
- User-friendly error responses
- Internal logging hooks

1.E Secrets & Environment Hardening — ✅ Done
- Secrets moved to .env
- Hardcoded DSNs removed
- Env validation added

------------------------------------------------------------
Phase 2 — Stabilization II

2.A Operational Stabilization — ✅ Done
- Oracle connection pooling (SessionPool)
- SQLite testing mode stability (baseline)
- Health readiness endpoint
- Lightweight request rate limiting

2.B Performance Stabilization — ✅ Done
- LLM latency path measurement
- DB roundtrip metrics
- Perf logs and `/health/perf` endpoint with averages

2.C Test Coverage — ✅ Done
- 17 passing tests (input, prompt, SQL validation, error handling, agent pipeline stub, sqlite run_sql)
- pytest + pytest-asyncio installed
- Coverage target baseline achieved (~smoke coverage)

2.C Test Coverage — ⏳ Pending
- 20–30% unit coverage
- ask() pipeline coverage
- Oracle/SQLite integration tests

------------------------------------------------------------
Phase 3 — UI / UX Enhancements
3.A Stateful Components — ⏳ Pending
- UI state persistence
- Progress components
- Auto-refresh mechanics

3.B Visualization Modules — ⏳ Pending
- Plotly integrations
- Data tables with pagination
- Export helpers

------------------------------------------------------------
Phase 4 — Deployment & Runtime
4.A Containerization — ⏳ Pending
- Dockerfile refinement
- Multi-stage builds

4.B Nginx Layer — ⏳ Pending
- Reverse proxy
- Static asset handling

4.C Service Installation — ⏳ Pending
- Windows service scripts
- Linux systemd integration

------------------------------------------------------------
Cross-Phase Tasks (Always Active) — 🚧 Ongoing
- Maintain agent_system_knowledge.md
- Update ADRs when decisions occur
- Log behavioral changes
- Enforce Agent Operating Contract, agent_rules.md, and Vanna compliance

------------------------------------------------------------
Summary Dashboard
- Phase 1: 5/5 completed
- Phase 2: 1/3 completed
- Phase 3: 0/2 completed
- Phase 4: 0/3 completed
- Cross-phase operations: active
