فيما يلي **README.md احترافي كامل** وجاهز لوضعه في مشروعك
`full_vanna_project/README.md`
وهو مكتوب بأسلوب شركات SaaS ويصلح للإنتاج Production-Grade.

---

# 📘 **Vanna AI – Production-Grade Agent System**

نظام متكامل يعتمد على Vanna AI لتقديم وكيل ذكي (AI Agent) قادر على:

* تشغيل نماذج لغوية متعددة (LM Studio – OpenAI – Groq – Gemini)
* الاتصال بعدة قواعد بيانات (SQLite – Oracle – MSSQL)
* تنفيذ استعلامات SQL
* إدارة ومعالجة البيانات
* التفاعل عبر واجهة ويب جاهزة من Vanna
* دعم الذاكرة باستخدام ChromaDB
* التشغيل عبر Docker و Nginx
* التشغيل كخدمة على Windows / Linux

النظام جاهز للاستخدام المباشر في بيئات الإنتاج.

---

# 🏗️ **Project Structure**

```
full_vanna_project/
│
├── app/
│   ├── main.py                 # Startup File (FastAPI + VannaFastAPIServer)
│   ├── config.py               # Global System Configuration (LLM + DB + Server)
│   │
│   ├── agent/
│   │   ├── builder.py          # Creates and assembles the Vanna Agent
│   │   ├── db.py               # Dynamic DB Provider (SQLite/Oracle/MSSQL)
│   │   ├── llm.py              # Dynamic LLM Provider (LMStudio/OpenAI/Groq/Gemini)
│   │   ├── memory.py           # ChromaDB Persistent Memory
│   │   ├── tools.py            # Tool Registry (SQL, Memory, Visualization, etc.)
│   │   ├── enrichers.py        # Context enrichers
│   │   ├── filters.py          # Sensitive data filters
│   │   ├── hooks.py            # Lifecycle hooks
│   │   ├── workflow.py         # Workflow handler (/help, commands…)
│   │   ├── port_guard.py       # Auto port-scanning & fallback
│   │   └── security.py         # Security utilities
│   │
│   ├── api/
│   │   ├── health.py           # Health Check Endpoint
│   │   ├── db_status.py        # Database Status Endpoint
│   │   ├── llm_status.py       # LLM Status Endpoint
│   │   └── router.py           # API Router (mounted under /api)
│   │
│   └── utils/
│       ├── helpers.py          # Helper utilities
│       └── logger.py           # System logger
│
├── docker/
│   ├── Dockerfile              # FastAPI Container
│   ├── docker-compose.yml      # Full stack (App + Nginx)
│   └── nginx/
│       └── nginx.conf          # Reverse Proxy (HTTP 80)
│
├── services/
│   ├── linux/                  # systemd service files
│   └── windows/                # Windows NSSM service wrappers
│
├── static/                     # Static files (default Vanna UI is bundled internally)
│
├── requirements.txt            # Complete Dependencies
├── .env                        # Environment Variables
└── README.md                   # This file
```

---

# ⚙️ **Features**

### ✓ Multiple LLM Providers

* LM Studio (local models)
* OpenAI (GPT-4 Turbo, GPT-4o…)
* Groq (Mixtral, LLaMA-3 Turbo)
* Google Gemini (Pro, Flash)

### ✓ Multiple Database Providers

* SQLite (افتراضي)
* Oracle (via cx_Oracle)
* MSSQL (via pyodbc)

### ✓ Production-Ready Memory

* ChromaDB vector memory (persistent)
* Supports long-term agent awareness

### ✓ Built-in Web UI from Vanna

* Chat interface
* SQL runner
* Data visualization
* Memory viewer
* File upload
* Agent tools inspector
  → لا تحتاج Frontend إضافي.

### ✓ DevOps Ready

* Dockerfile
* docker-compose (App + Nginx)
* Nginx Reverse Proxy (HTTP 80)
* systemd service (Linux)
* NSSM-based service (Windows)

### ✓ Security

* Sensitive data filter
* Config via environment variables
* CORS configurable

---

# 🚀 **How to Run (Local Development)**

## 1️⃣ إنشاء بيئة افتراضية:

```
python -m venv venv
```

```
venv\Scripts\activate   # Windows
source venv/bin/activate # Linux/Mac
```

## 2️⃣ تثبيت المتطلبات:

```
pip install -r requirements.txt
```

## 3️⃣ تشغيل التطبيق:

```
python -m app.main
```

## 4️⃣ الوصول إلى الواجهة:

```
http://localhost:8000/vanna
```

---

# 🐳 **Running with Docker**

## 1️⃣ Build & Run

```
docker-compose up --build
```

## 2️⃣ Visit Frontend

```
http://localhost/
```

---

# 🔧 **Environment Variables (.env)**

أهم المتغيرات:

```
HOST=0.0.0.0
PORT=8000

DB_PROVIDER=sqlite
SQLITE_DB=D:\mydb.db

LLM_PROVIDER=lmstudio
LM_STUDIO_URL=http://10.10.10.1:1234/v1
LM_STUDIO_MODEL=gemma-3n

OPENAI_API_KEY=...
GROQ_API_KEY=...
GEMINI_API_KEY=...

AGENT_MEMORY_MAX_ITEMS=1000
```

---

# 💾 **Database Selection**

الاختيار يتم تلقائيًا عبر:

```
DB_PROVIDER=sqlite | oracle | mssql
```

---

# 🤖 **LLM Selection**

تغيير مزود النموذج:

```
LLM_PROVIDER=lmstudio | openai | groq | gemini
```

---

# 🧠 **Memory**

ChromaDB يتم تشغيله تلقائياً في:

```
./chroma_db/
```

---

# 🧩 **API Endpoints**

### Health:

```
GET /api/health
```

### LLM Status:

```
GET /api/llm-status
```

### DB Status:

```
GET /api/db-status
```

---

# 🛡️ **Production Deployment Notes**

* يفضل وضع Nginx أمام التطبيق
* دعم SSL يمكن إضافته بسهولة لاحقاً
* يمكن استخدام Supervisor أو systemd أو NSSM لتشغيله كخدمة

---

# 📞 **Support**

للمساعدة أو التخصيص أو إضافة ميزات جديدة:
يرجى التواصل مباشرة.

---


# Deployment Options

Method A � Docker (app + nginx)
- Build/start: docker compose up -d --build`n- Access: http://localhost:8080 (charts served from /charts )
- Volumes: ./chroma_db -> /app/chroma_db, ./app/static/charts -> /app/app/static/charts`n- Healthcheck: /api/health/ready`n
Method B � Native (no Docker)
- Ensure venv and .env exist.
- Run: scripts\run_prod.bat (uvicorn on 0.0.0.0:8000, workers=2)
- Access UI: http://localhost:8000`n
