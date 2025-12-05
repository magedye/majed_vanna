## OPS_SOP — Majed Vanna Maintenance Procedures

### 1) Secrets & Env Rotation
- Edit `.env` with new secrets (Oracle password, LM Studio key if applicable).
- Restart backend (`scripts/run_prod.bat`).

### 2) Backup & Restore (ChromaDB)
- Backup (admin required): `POST /api/system/backup-memory` (set `vanna_email=admin@example.com` cookie/header).
- Restore: stop backend, replace `./backups/...` into `./chroma_db`, restart backend.

### 3) Memory Reset & Retrain
- Reset (admin): `DELETE /api/system/reset-memory?force=true`.
- Retrain: `python scripts/train_local.py` (Oracle schema governed by ORACLE_TRAIN_* env).
- Restart backend after retrain.

### 4) Admin Role Control
- Admin is validated via `vanna_email` cookie/header == `admin@example.com`.
- Change admin: update the check in `app/api/system_ops.py` and redeploy.

### 5) Health & Metrics
- Health: `GET /api/health/ready` (includes Oracle status, LLM latency, vector_store readiness, trace_id).
- Metrics: `GET /api/metrics`.

### 6) Breaker States & Recovery
- LLM breaker: opens after consecutive failures; reset_timeout=30s. Restore LM Studio, wait, retry.
- DB breaker: opens on repeated Oracle failures; fix connectivity, wait for reset, retry.

### 7) Log Locations
- JSON logs to stdout (server console). Include trace_id/span_id.
- Audit: `audit.log` for agent events (if enabled).

### 8) Payload/Rate Controls
- Payload cap: `MAX_PAYLOAD_SIZE_BYTES` (middleware).
- Rate limit: `RATE_LIMIT_MAX_REQUESTS` / `RATE_LIMIT_WINDOW_SECONDS`.
