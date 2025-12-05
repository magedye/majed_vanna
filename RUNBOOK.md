## RUNBOOK — Majed Vanna Production Ops

### Quick Reference
- Start: `scripts/run_prod.bat` (port 7777, kills conflicting PID)
- Stop: `Ctrl+C` or kill PID; graceful shutdown closes Oracle pool
- Health: `GET /api/health/ready` (Oracle, LLM latency, vector_store, trace_id)
- Metrics: `GET /api/metrics`
- Memory ops (admin only): `/api/system/backup-memory`, `/api/system/reset-memory?force=true` (requires `vanna_email=admin@example.com`)

### Breakers & Timeouts
- LLM CircuitBreaker: opens after repeated failures; reset_timeout=30s; retries/backoff configured via env `LLM_*`.
- DB CircuitBreaker: wraps Oracle connections; retries/backoff via `DB_*`.
- Timeouts: `LLM_TIMEOUT_MS` (default 60000), `DB_QUERY_TIMEOUT_MS` (default 30000).

### Payload & Rate
- Max payload: `MAX_PAYLOAD_SIZE_BYTES` (default 1MB) enforced by middleware.
- Rate limit: configured via env `RATE_LIMIT_MAX_REQUESTS` / `RATE_LIMIT_WINDOW_SECONDS`.

### Logs & Trace
- JSON logs include `trace_id`/`span_id`.
- Slow requests logged at WARN when exceeding `SLOW_REQUEST_THRESHOLD_MS` (default 2000ms).

### Chroma/Memory
- Backup: `POST /api/system/backup-memory` (admin).
- Reset: `DELETE /api/system/reset-memory?force=true` (admin). Restart backend afterward.
- Retrain: `python scripts/train_local.py` (uses Oracle when DB_PROVIDER=oracle).

### Troubleshooting
- Health error (db): check Oracle creds/DSN; CircuitBreaker may be OPEN if repeated failures.
- Health LLM unknown: trigger an LLM call to gather latency; ensure LM Studio reachable.
- Payload too large: reduce request size or raise `MAX_PAYLOAD_SIZE_BYTES`.
- CSP/HSTS headers enforced by middleware; adjust only if frontend requires.
