## **Components Reference**

### **1. Agent Layer**
- `builder.py` — agent construction
- `workflow.py` — message → tool routing
- `security.py` — permission validation
- `memory.py` — session isolation

### **2. Tools Layer**
- `db.py` — SQL executor
- `tools.py` — utility tools
- `metadata providers` — Oracle, SQLite, DataHub, dbt

### **3. API Layer**
- `router.py` — all routes
- `metadata.py` — schema extraction interface

### **4. UI Layer**
- `static/index.html`
- `vanna-components.js`

### **5. Utility Layer**
- `logger.py` — structured logging
- `helpers.py` — request helpers
