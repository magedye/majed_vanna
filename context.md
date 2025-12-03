فيما يلي **ملف CONTEXT.md كامل وشامل** — جاهز لوضعه داخل مشروعك
`full_vanna_project/CONTEXT.md`

هذا الملف مكتوب بأسلوب هندسي احترافي، ويُعتبر **وثيقة مرجعية عليا** للمشروع:

* يشرح الوضع الحالي
* خيارات التطوير الأخيرة
* إمكانية تطبيقها
* المتطلبات الفنية
* خارطة الطريق
* الاعتبارات المعمارية
* التكامل مع Oracle في بيئة بنكية
* مقارنة WrenAI
* اتجاهات التطوير القادمة

---

# 📘 **CONTEXT.md – Vanna Production AI System (Full Technical Context)**

## 📌 **1. Overview**

هذا المشروع يمثل نظامًا إنتاجيًا متكاملاً مبنيًا على:

* **Vanna AI Agent**
* **FastAPI Backend**
* **ChromaDB Memory**
* **LLM Provider Abstraction (LM Studio, OpenAI, Groq, Gemini)**
* **Multiple Database Providers (SQLite, Oracle, MSSQL)**
* **Production Runtime (Docker, Nginx, Services)**
* **Vanna Web UI (Integrated)**

الهدف النهائي:
**نظام ذكاء أعمال + Agent قادر على العمل فوق بيئة بيانات بنكية باستخدام Oracle Database.**

---

# 📌 **2. Current Architecture Summary**

## 🧩 Core Components

| Layer      | Implementation                                  | Status |
| ---------- | ----------------------------------------------- | ------ |
| API Server | FastAPI                                         | ✔ جاهز |
| Agent      | Vanna Agent with tools                          | ✔ جاهز |
| Memory     | ChromaDB                                        | ✔ جاهز |
| DB Layer   | Oracle, SQLite, MSSQL via dynamic provider      | ✔ جاهز |
| LLM Layer  | LM Studio / OpenAI / Groq / Gemini              | ✔ جاهز |
| Web UI     | Vanna Built-in                                  | ✔ جاهز |
| Deployment | Docker, Nginx (port 80), Windows/Linux services | ✔ جاهز |

---

# 📌 **3. Key Development Options (Recent Technical Choices)**

هذه هي الخيارات التطويرية التي ناقشناها، مع تقييم إمكانية تطبيق كل خيار، وماذا يحتاج فنيًا.

---

## 🟦 **Option A — Use Built-in Vanna UI (Current Choice)**

### ✔ إمكانية التطبيق:

جاهز فورًا — تم دمجه بالفعل.

### ✔ ماذا يقدم:

* Chat
* SQL Runner
* Visualization
* Upload
* Memory Tools
* Tool invocation inspection

### ✔ الاحتياجات:

لا شيء إضافي.

### ❗ ماذا لا يقدّم:

* لا يدعم تغيير DB/LLM من الواجهة
* لا يحتوي Dashboard Status
* لا يحتوي BI Dashboards
* لا يوجد Intent Engine
* لا يوجد Semantic Modeling Layer

---

## 🟩 **Option B — Add Semantic Understanding Layer (Not activated yet)**

يشبه ما يفعله Wren Engine في WrenAI.

### ✔ إمكانية التطبيق:

ممكن بنسبة **100%** داخل المشروع الحالي.

### ✔ الفائدة:

* تحسين دقة Text-to-SQL
* فهم الأسئلة البنكية المعقدة
* Intent Detection (query/chat/summary/admin)
* Entity Extraction (جدول/عمود/تاريخ/كيانات مالية)
* Routing للأدوات وقدرات agent

### ✔ الاحتياجات الفنية:

#### ملفات جديدة:

```
app/agent/semantic/
    ├── intent_detector.py
    ├── entity_extractor.py
    ├── semantic_parser.py
    ├── query_router.py
```

#### المتطلبات:

* تصميم **Entity Schema** (الجداول والعلاقات)
* تحليل **Oracle Metadata**
* بناء **Domain Dictionary** للنطاق البنكي
* تدريب prompts خاصة للـ LLM

### ⚠️ التقدير:

متوسط — يحتاج 2–4 أيام هندسية.

---

## 🟧 **Option C — Add BI Dashboard (Wren-like Mini BI Layer)**

يقترب من WrenAI ولكن أخف.

### ✔ إمكانية التطبيق:

ممكن، لكنه **أكبر من Option B**.

### ✔ الفائدة:

* Text-to-Chart
* Dashboard panels
* Insights
* Summaries
* Time-series graphs

### ✔ الاحتياجات:

* بناء صفحات جديدة:

```
dashboard/index.html
dashboard/charts.html
dashboard/metrics.html
```

* بناء Chart Engine (Plotly / ECharts)
* بناء endpoints:

```
/api/bi/query
/api/bi/chart
/api/bi/summary
```

### ⚠️ التقدير:

بناء BI خفيف: 4–7 أيام
بناء BI متوسط: 10–14 يوم
(WrenAI-level BI يستغرق أسابيع)

---

## 🟨 **Option D — Add DB & LLM Switching UI Page**

صفحة لإدارة الإعدادات:

### ✔ إمكانية التطبيق:

ممتاز — سهل جدًا.

### ✔ الفائدة:

* اختيار DB Provider من الواجهة
* اختيار LLM Provider
* تغيير config بدون فتح ملفات
* زر لإعادة تشغيل الخدمة

### ✔ الاحتياجات:

* صفحة settings.html
* endpoints:

```
GET/POST /api/settings
POST /api/restart
```

### ⚠️ التقدير:

3–6 ساعات فقط.

---

## 🟫 **Option E — WrenAI-Style Semantic BI Platform (Full)**

هذا يعادل بناء **نظام يشبه WrenAI بالكامل**.

### ✔ إمكانية التطبيق:

ممكن نظريًا، لكن يحتاج جهد نظام شركات.

### ✔ الاحتياجات الهندسية:

* Metadata Layer
* Semantic Modeling Engine
* Metrics Engine
* Join Graph Engine
* Query Planner
* Chart Intelligence
* BI Dashboard
* Permissions/Governance
* Multi-source virtualization

### ⚠️ التقدير:

مشروع ضخم — يحتاج أسابيع أو أشهر.

---

# 📌 **4. Oracle-Specific Considerations (Banking Environment)**

## ✔ متطلبات تشغيل Oracle في بيئة بنكية:

* DSN ثابت + ODP configuration
* قيود صلاحيات (User Roles)
* حماية Queries
* Audit logging
* Masking للبيانات الحساسة
* Metadata extraction
* Query Whitelisting
* استعلامات آمنة
* لا توجد dynamic table injections

### لماذا هذا مهم؟

لأن النظام سيتعامل مع:

* حسابات
* معاملات
* أرصدة
* بيانات حساسة
* بيانات زمنية

لذلك يجب استخدام:

* Semantic Layer لأن Text-to-SQL العادي قد يكون خطيرًا
* Tools محدودة
* SQL Sanitization
* Audit logging للعمليات

---

# 📌 **5. Technical Requirements for Each Feature**

## Semantic Layer:

* Build metadata map (tables, columns, PK/FK)
* Build intent detector (LLM or rule-based)
* Build entity extractor (NER + regex + DB schema)
* Build semantic parser
* Build router
* Integrate with Vanna Agent Tools

## BI Layer:

* Chart generator
* Summary engine
* Metric definitions
* Dashboard UX
* Security layer
* Endpoint orchestration

## Settings UI:

* Frontend (HTML/Jinja/Tailwind)
* Backend settings API
* Config parser/updater
* Service restart trigger

---

# 📌 **6. Where the Current Project Stands**

حالياً:

✔ جاهز للإنتاج
✔ جاهز للعمل على Oracle
✔ LLM abstraction قوي
✔ Memory متقدمة (ChromaDB)
✔ Web UI مدمجة جاهزة
✔ Tools قوية (SQL + Visualization + Memory)
✔ بنية Agent منظمة
✔ Docker + Nginx + Services جاهزة

النقص الوحيد إذا نريد WrenAI-like system:

* Semantic Modeling Layer
* BI Dashboard (اختياري)
* Settings UI (optional but useful)

---

# 📌 **7. Recommended Path Based on Requirements**

## إذا كان هدفك: "Oracle Banking AI Agent"

أنصح بـ:

### Phase 1:

✔ إضافة Semantic Layer خفيف (Intent + Entity + Parser + Router)

### Phase 2:

✔ إضافة Settings UI لتغيير DB/LLM بسهولة

### Phase 3:

✔ دعم Charts وSummary كنواة BI بسيطة (Mini WrenAI)

### Phase 4:

❗ إذا رغبت — بناء BI كامل بمرور الوقت

---

# 📌 **8. Summary of Implementation Feasibility**

| Feature                | Difficulty  | Feasible? | Notes                 |
| ---------------------- | ----------- | --------- | --------------------- |
| Semantic Layer         | Medium      | ✔ 100%    | أعلى قيمة مقابل الجهد |
| BI Dashboard           | Medium/High | ✔         | يحتاج وقت             |
| Settings UI            | Low         | ✔         | مهم وعملي             |
| Full WrenAI Equivalent | High        | ✔         | مشروع كبير            |

---

# 📌 **9. Conclusion**

هذا الملف يمثّل:

* الأساس الفني للمشروع
* الخلفية التقنية لاتخاذ القرارات
* تقييم واقعي لخيارات التطوير
* خارطة طريق مستقبلية
* التزامات Oracle البنكية
* مقارنة مع WrenAI
* إمكانيات وقيود النظام

ويمكن الاعتماد عليه لفتح محادثات جديدة دون فقد السياق.

-