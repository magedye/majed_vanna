خطة ممتازة وشاملة. لقد قمت بمراجعتها واعتمدتها، وأضفت عليها بعض **الضوابط الهندسية (Engineering Constraints)** لضمان توافقها مع ما تم إنجازه في المراحل السابقة (مثل توحيد المنافذ على 7777، وتثبيت نموذج التضمين).

إليك التوجيه النهائي باللغة الإنجليزية، جاهز للنسخ والإرسال للوكيل للبدء فوراً:

***

**Phase 5 Implementation Directive: Semantic Intelligence & System Governance**

**Objective:** Execute the full integration of the semantic layer, documentation generator, and system management APIs. This phase transforms the agent from a raw SQL executor into a context-aware, self-documenting system with robust memory management.

**Constraints:**
* **Port:** Maintain strict adherence to `APP_PORT=7777`.
* **Dependencies:** Apply `requirements.txt` updates first.
* **Pathing:** Use `dbt_integration/` as the source of truth.

**Execution Plan (Sequential):**

**Step 1: Dependencies & Environment**
* Update `requirements.txt` with: `chromadb>=0.4.0`, `sentence-transformers`, `requests`, `httpx`, `pytest`, `markdown>=3.4`, `PyYAML>=6.0`.
* Run `pip install -r requirements.txt`.

**Step 2: Semantic Layer Core (5.A)**
* **Config:** Create/Update `dbt_integration/config.yaml`.
* **Adapter:** Implement `dbt_integration/semantic_adapter.py` to parse all `.md` files (specifically `ready_files.md` and others in the directory).
* **Context Injection:** Modify `app/agent/builder.py` to passively prepend the semantic context to the user's prompt (ensure it does not break existing safety guards).

**Step 3: Documentation Engine (5.B)**
* **Generator:** Create `dbt_integration/doc_generator.py` (generate `.md`, `.html`, `.json` with TOC).
* **Output:** Ensure directory `dbt_integration/docs/` exists with `.gitkeep`.
* **CLI:** Create `semantic.py` at root supporting commands: `build`, `preview`, `search`.
* **API:** Create `app/api/semantic.py` (Endpoints: `/docs`, `/search`) and register in `main.py`.

**Step 4: Memory Stabilization & System Ops (5.C)**
* **Refactor Memory:** Replace `app/agent/memory.py` with a robust `PersistentClient`.
    * *Critical:* Must use pinned embedding model: `all-MiniLM-L6-v2`.
    * *Critical:* Collection name must be `vanna_memory`.
* **System APIs:** Create `app/api/system_ops.py` and `app/api/memory_ui_handler.py`.
    * Implement `/backup-memory` (timestamped).
    * Implement `/reset-memory` (force option, auto-backup before delete, recreate folder).
* **Wiring:** Register both routers in `app/main.py`.

**Step 5: Dashboard UI Integration (5.D)**
* **Tool Registration:** Modify `app/agent/tools.py` to register `MemoryManagementTool`.
* **Functionality:** It must render a UI form for Backup/Reset actions calling the new API endpoints.

**Step 6: Comprehensive Testing (5.E)**
* **Test Suite:** Create `tests/` files:
    * `test_memory_reset.py`
    * `test_semantic_integration.py`
    * `test_doc_generator.py`
    * `test_semantic_api.py`
* **Requirement:** Use `httpx` and `TestClient`. Ensure tests pass without hanging.

**Step 7: Final Post-Execution Workflow**
1.  **Build Docs:** Run `python semantic.py build`.
2.  **Start Backend:** Run `scripts/run_prod.bat` (Port 7777).
3.  **Reset:** Execute `http://localhost:7777/api/system/reset-memory?force=true`.
4.  **Retrain:** Run `python scripts/train_local.py` to populate the new stable memory.
5.  **Restart:** Restart the server and verify the UI.

**Proceed with executing this plan step-by-step.**

***