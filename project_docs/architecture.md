## **System Architecture — Majed Vanna Project**

### **Layers**

#### 1. **UI Layer**
- `<vanna-chat>` web component
- React-based admin UI (optional future)
- Delivered via FastAPI static hosting

#### 2. **API Layer (FastAPI)**
- Chat endpoints
- Health & status
- Metadata endpoints
- Middleware for identity, quota, input validation

#### 3. **Agent Layer**
- Workflow manager
- Security filters (Phase 1)
- Memory/session manager
- Tool selector

#### 4. **Tools Layer**
- SQL Executor
- Metadata Providers (Oracle, SQLite, dbt, DataHub)
- File/OS/API utilities
- Visualization/Artifact generator

#### 5. **LLM Layer**
- LM Studio via OpenAI-compatible REST
- Summary transformations
- Prompt safety filters

### **Data Flow Summary**
```
User → FastAPI → Security → Workflow → Tool → LLM (summary) → UI Artifact → Frontend
```

### **Key Architectural Guarantees**
- Zero breaking changes during phased rollout.
- Strict module-to-module boundaries.
- Security-first pipeline.