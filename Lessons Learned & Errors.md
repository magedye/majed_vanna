# Lessons Learned & Errors

## 1. Workflow handler compatibility
- **Issue:** `TriggerResult` is no longer exposed by `vanna.core.workflow`, so `app/agent/workflow.py` failed with `ImportError`.
- **Fix:** Switch to returning `WorkflowResult` (see `app/agent/workflow.py:1-11`); explicit `should_skip_llm` flags preserve the command response while matching the current API.

## 2. Tool context enrichment
- **Issue:** Treating `ToolContext` as a mutable dict caused `TypeError: 'ToolContext' object does not support item assignment` when `TimezoneEnricher` executed.
- **Fix:** Write to `context.metadata` instead; the metadata dict is meant for auxiliary data and keeps the `ToolContext` immutable semantics (`app/agent/enrichers.py:1-7`).

## 3. Observability provider stub
- **Issue:** The crude lambda stub called `Span("span", {})`, which passed positional args to `pydantic.BaseModel` and raised `BaseModel.__init__() takes 1 positional argument but 3 were given`.
- **Fix:** Implement a `DummyObservability` subclass that overrides the async methods and builds `Span(name=name, attributes=...)` with keyword args, matching `vanna.core.observability.base.ObservabilityProvider` expectations (`app/agent/builder.py:29-49`).

## 4. Environment and dependency handling
- **Issue:** Running `python app/main.py` outside of the virtual environment could not find `pyodbc` even though it was listed in `requirements.txt`.
- **Fix:** Activate the `venv` or call `venv\Scripts\python.exe` before running the app. Keep `pip install -r requirements.txt` inside the venv to ensure MSSQL/Oracle drivers are available.

## 5. Shared issues with `full_vanna_project_OK`
- The alternate codebase (`D:/full_vanna_project_OK`) still imports `TriggerResult`, mutates `ToolContext` directly, and instantiates `Span` with positional args, so the same runtime errors would recur unless the above fixes are applied there too. Their repo also adds useful health/llm/db endpoints and port-guard logic, but the foundational bugs must be resolved first.

## Next Actions
1. Copy these fixes into any new project scaffold before starting work to avoid the same runtime failures.
2. Add regression tests (workflow handler, enrichers, observability) to catch interface changes in future `vanna` releases.
3. Automate venv activation (e.g., via scripts) so contributors reliably install `requirements.txt` in the correct interpreter.



# Lessons Learned & Errors

## 1. Workflow handler compatibility
- **Issue:** `TriggerResult` is no longer exposed by `vanna.core.workflow`, so `app/agent/workflow.py` failed with `ImportError`.
- **Fix:** Switch to returning `WorkflowResult` (see `app/agent/workflow.py:1-11`); explicit `should_skip_llm` flags preserve the command response while matching the current API.

## 2. Tool context enrichment
- **Issue:** Treating `ToolContext` as a mutable dict caused `TypeError: 'ToolContext' object does not support item assignment` when `TimezoneEnricher` executed.
- **Fix:** Write to `context.metadata` instead; the metadata dict is meant for auxiliary data and keeps the `ToolContext` immutable semantics (`app/agent/enrichers.py:1-7`).

## 3. Observability provider stub
- **Issue:** The crude lambda stub called `Span("span", {})`, which passed positional args to `pydantic.BaseModel` and raised `BaseModel.__init__() takes 1 positional argument but 3 were given`.
- **Fix:** Implement a `DummyObservability` subclass that overrides the async methods and builds `Span(name=name, attributes=...)` with keyword args, matching `vanna.core.observability.base.ObservabilityProvider` expectations (`app/agent/builder.py:29-49`).

## 4. Environment and dependency handling
- **Issue:** Running `python app/main.py` outside of the virtual environment could not find `pyodbc` even though it was listed in `requirements.txt`.
- **Fix:** Activate the `venv` or call `venv\Scripts\python.exe` before running the app. Keep `pip install -r requirements.txt` inside the venv to ensure MSSQL/Oracle drivers are available.

## 5. Shared issues with `full_vanna_project_OK`
- The alternate codebase (`D:/full_vanna_project_OK`) still imports `TriggerResult`, mutates `ToolContext` directly, and instantiates `Span` with positional args, so the same runtime errors would recur unless the above fixes are applied there too. Their repo also adds useful health/llm/db endpoints and port-guard logic, but the foundational bugs must be resolved first.

## Next Actions
1. Copy these fixes into any new project scaffold before starting work to avoid the same runtime failures.
2. Add regression tests (workflow handler, enrichers, observability) to catch interface changes in future `vanna` releases.
3. Automate venv activation (e.g., via scripts) so contributors reliably install `requirements.txt` in the correct interpreter.
