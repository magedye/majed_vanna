Role: Senior Python Backend Engineer & Semantic Layer Integration Specialist
Project: majed_vanna
Objective: Execute full integration of the semantic layer + documentation generator + system management APIs, based strictly on all files inside:
dbt_integration/
including ready_files.md, and ensuring compatibility with Vanna, FastAPI, and the local ChromaDB memory layer.

⚠️ Pre-Execution Requirements (MANDATORY)

Before modifying any file, update requirements.txt:

chromadb>=0.4.0
sentence-transformers
requests
httpx
pytest
markdown>=3.4
PyYAML>=6.0


Then run:

pip install -r requirements.txt


Important:
The UI memory handler uses a fixed port: http://localhost:7777/….
Keep your backend running on port 7777 to avoid breaking the Reset/Backup buttons.

📂 Integration Plan — Execute EXACTLY in this order
✅ Step 1 — Install and Configure Semantic Layer Core

Create or update:

dbt_integration/config.yaml

dbt_integration/semantic_adapter.py

Use all semantic files found under:

dbt_integration/


including:

semantic_layer_final_plan.md

documentation_index.md

quick_start_guide.md

short_summary.md

code_implementation_package.md

vana_cbtcore.md

ready_files.md ← MUST be included
(as referenced in ready_files.md itself 

ready_files

)

Implement passive context injection:

Modify app/agent/builder.py

Inject semantic context in before_llm_request

Prepend context to user_msg.content only

✅ Step 2 — Auto-Documentation Generator

Implement the full module:

dbt_integration/doc_generator.py

Create directory: dbt_integration/docs/

Add: dbt_integration/docs/.gitkeep

Capabilities required:

Merge all semantic files into one unified:

semantic_docs.md

semantic_docs.html

semantic_docs.json

Build Table of Contents

Extract section headers

Support CLI + API

Update config.yaml with:

documentation_output_path: "./dbt_integration/docs/"
documentation_formats: ["md", "html", "json"]

✅ Step 3 — Add CLI Entry Point

Create the file at project root:

semantic.py


with commands:

python semantic.py build
python semantic.py preview
python semantic.py search "<keyword>"


These commands must call SemanticDocGenerator.

✅ Step 4 — Add Semantic Documentation API

Create:

app/api/semantic.py


Add endpoints:

GET /api/semantic/docs
GET /api/semantic/search?query=<keyword>


Then register router in:

app/main.py

✅ Step 5 — Memory Stabilization Layer

Replace the entire content of:

app/agent/memory.py


Ensure:

PersistentClient

embedding pinned: all-MiniLM-L6-v2

collection name: vanna_memory

safe initialization

user-friendly error messages

Ensure this is compatible with your existing LocalVanna setup.

✅ Step 6 — System Management APIs

Create:

app/api/system_ops.py
app/api/memory_ui_handler.py


Features required:

/api/system/backup-memory

/api/system/reset-memory?force=true

UI-executed backup/reset for Dashboard

Automatic timestamped backups

Reset action backed by auto-backup

Recreate chroma_db folder after purge

Add both routers to:

app/main.py

✅ Step 7 — UI Integration

In:

app/agent/tools.py


register:

MemoryManagementTool


This should:

Show a UI form

Allow backup/reset actions

Use the /api/system/execute-memory-op endpoint

Ensure compatibility with your UiComponent-based Vanna dashboard.

✅ Step 8 — Test Suite Integration

Add:

tests/test_memory_reset.py
tests/test_semantic_integration.py
tests/test_doc_generator.py
tests/test_semantic_api.py


Tests must validate:

Safe memory reset

Backup creation

Semantic context loading

Unified documentation generation

API endpoints

No crashes when semantic layer disabled

Use httpx + TestClient.

✅ Step 9 — Regenerate Documentation

After integrating everything, run:

python semantic.py build


Verify files:

dbt_integration/docs/semantic_docs.md
dbt_integration/docs/semantic_docs.html
dbt_integration/docs/semantic_docs.json

✅ Step 10 — Final Post-Execution Steps

Start backend:

python app/main.py


Reset memory once:

http://localhost:7777/api/system/reset-memory?force=true


Re-train embeddings:

python scripts/train_local.py


Restart backend again:

Ctrl+C
python app/main.py

📌 Additional Requirements

Ensure ready_files.md is incorporated into the semantic model indexing (mandatory) 

ready_files

Ensure cross-platform paths remain valid (Path, not only os.path)

Keep logs minimal but explicit

Do NOT alter core Vanna agent logic

Preserve passive mode (no SQL generation)

🟩 Output Expected from the Agent

Once finished:

All files are created or updated

All routers wired

All tests pass

Semantic layer fully operational

Documentation generator functional

Dashboard Memory Manager visible

No ChromaDB mismatch

No import errors

Ready for production-level local development integration
