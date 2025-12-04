Roadmap & Operational Tasks

Project: Majed Vanna Enterprise System
Maintained by: Autonomous Agent (under contract)
Last Updated: {auto-update by agent}

Legend
- ƒo. Done
- dYs In Progress
- ƒ?3 Pending
- ƒ>" Blocked / Requires Human Approval

------------------------------------------------------------
Phase 1 ƒ?" Core Stabilization (ƒo. 5/5 complete)

1.A Input Safety Layer ƒ?" ƒo. Done
- Message sanitization
- Metadata validation
- ID rules
- FastAPI middleware integration
- SafeChatHandler activation

1.B SQL Safety Layer ƒ?" ƒo. Done
- Single-statement enforcement
- Block destructive keywords
- Comment + tautology filters
- SafeRunSqlTool wrapper

1.C Prompt Safety Layer ƒ?" ƒo. Done
- Regex/rule filters
- Meta-instruction blocks
- Control-char stripping

1.D Unified Error Handling ƒ?" ƒo. Done
- API-level handlers
- User-friendly error responses
- Internal logging hooks

1.E Secrets & Environment Hardening ƒ?" ƒo. Done
- Secrets moved to .env
- Hardcoded DSNs removed
- Env validation added

------------------------------------------------------------
Phase 2 ƒ?" Stabilization II (ƒo. 3/3 complete)

2.A Operational Stabilization ƒ?" ƒo. Done
- Oracle connection pooling (SessionPool)
- SQLite testing mode stability (baseline)
- Health readiness endpoint
- Lightweight request rate limiting

2.B Performance Stabilization ƒ?" ƒo. Done
- LLM latency path measurement
- DB roundtrip metrics
- Perf logs and `/health/perf` endpoint with averages
- Context injection adapter wired to local ChromaDB + LM Studio

2.C Test Coverage ƒ?" ƒo. Done
- 17 passing tests (input, prompt, SQL validation, error handling, agent pipeline stub, sqlite run_sql)
- pytest + pytest-asyncio installed
- Added context injection tests (schema injection, truncation protection, logging)
- Coverage target baseline achieved (~smoke coverage)

------------------------------------------------------------
Phase 3 ƒ?" UI / UX Enhancements
3.A Secure Visualization Backend ƒo. Done
- SafeVisualizer writes to sandboxed `app/static/charts/<user_hash>/`
- Filename sanitization and user hashing guard traversal
- Chart payload persisted as JSON for reuse

3.B Frontend Visualization Integration ƒo. Done
- Charts exposed via FastAPI StaticFiles at `/charts`
- SafeVisualizer returns `chart_url` metadata for saved outputs
- Inline ChartComponent preserved for immediate rendering

------------------------------------------------------------
Phase 4 ƒ?" Deployment & Runtime
4.A Containerization ƒ?" ƒ?3 Pending
- Dockerfile refinement
- Multi-stage builds

4.B Nginx Layer ƒ?" ƒ?3 Pending
- Reverse proxy
- Static asset handling

4.C Service Installation ƒ?" ƒ?3 Pending
- Windows service scripts
- Linux systemd integration

------------------------------------------------------------
Cross-Phase Tasks (Always Active) ƒ?" dYs Ongoing
- Maintain agent_system_knowledge.md
- Update ADRs when decisions occur
- Log behavioral changes
- Enforce Agent Operating Contract, agent_rules.md, and Vanna compliance

------------------------------------------------------------
Summary Dashboard
- Phase 1: 5/5 completed
- Phase 2: 3/3 completed
- Phase 3: 2/2 completed
- Phase 4: 0/3 completed
- Cross-phase operations: active
