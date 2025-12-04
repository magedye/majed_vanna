فيما يلي فهم شامل + إعادة تنظيم + تحليل معماري لما ورد في وصف Vanna How It Works،
مع تقديمه داخل جدول احترافي يوضح:

المفهوم ووظيفته

كيف يتحقق فعليًا داخل مشروعك (Majed Vanna)

ما هي مكونات المشروع التي تخدمه

العلاقات والتسلسل بين المكوّنات

✅ الجدول الكامل — شرح هندسي لكيف تعمل المنظومة داخل مشروعك

هذا الجدول ليس تكرارًا للنص الأصلي، بل إعادة تفسيره معماريًا بناءً على مشروعك الحالي وهيكليته الفعلية.

🔵 القسم الأول — مسار التنفيذ الأساسي (Execution Pipeline)
العنصر	المفهوم	كيف يتحقق داخل مشروعك فعليًا	مكونات المشروع المشاركة	العلاقة بين المكونات
Your App → <vanna-chat>	مكوّن جاهز يُدرج داخل تطبيقك لبدء التفاعل	يتم تضمينه داخل صفحة الواجهة static/index.html أو واجهة React المستقبلية	static/, frontend, app/main.py	المستخدم يتفاعل عبر هذا المكوّن → المكوّن يرسل الطلب للـ API الخاص بك
User-Aware Agent	الوكيل يفهم هوية المستخدم، صلاحياته، الحصة المسموح بها	سيتم تنفيذ ذلك عبر: middleware + token verification + permission map داخل app/agent/security.py	app/agent/security.py, app/runtime.py, app/utils/logger.py	يلتقط الطلب → يتحقق من الهوية والصلاحيات → يمرّر الطلب للوكيل المناسب
Your Tools	الأدوات التي يستدعيها الوكيل لتنفيذ مهام المستخدم	أدوات المشروع: • SQL execution • metadata providers • file ops • enrichment tools	app/agent/tools.py, app/agent/db.py, app/agent/workflow.py	الوكيل ينفذ الطلب → يستدعي الأدوات المناسبة بناءً على السياق
Rich UI	الواجهة تعرض نتائج غنية (جداول، مخططات، عناصر تفاعلية)	يظهر في واجهة المشروع عبر: tables, charts, lineage view	static/, frontend/pages/*, Vanna-rendered components	الأدوات تُرجع نتائج خام → LLM يعطي summary → الواجهة تعرض artifact التفاعلي للمستخدم
🟣 القسم الثاني — مبدأ "User-Aware Execution"
العنصر	المفهوم	كيف يتحقق داخل مشروعك	الملفات المساهمة	العلاقة
User identity drives execution	كل طلب يحتوي على: user_id + permissions + workspace context	إضافة middleware في FastAPI لتضمين user_id داخل كل request، ثم تمريره لـ agent context	app/main.py, app/agent/security.py, future middleware/auth.py	الطلب → middleware → agent workflow → tool execution
Automatic permission checking	الأدوات نفسها تتحقق من الصلاحيات	إضافة decorator مثل: @require_permission("sql.query")	app/agent/security.py, app/agent/tools.py	workflow → tool → security layer
Conversation isolation	كل مستخدم له session خاص	باستخدام session_id داخل memory provider	app/agent/memory.py	memory tied to user/session
Quota limits	تحديد عدد الاستعلامات / زمن التنفيذ	تُطبق عبر rate limits عند API المدخل	app/main.py, FastAPI + SlowAPI	API → security → execution throttling
🟡 القسم الثالث — تجربة الواجهة (UI State Model)
العنصر	المفهوم	كيف يتحقق داخل مشروعك	الملفات	العلاقة
Components update, not append	النتائج لا تُضاف كرسائل فقط، بل تحديث لحالات UI stateful	React components: tables, lineage, status cards ستعمل كـ stateful widgets	frontend/components/*, static/vanna-components.js	agent output → rendered artifacts → UI updates state
Progress bars, status updates	workflow يعيد حالة التنفيذ تلقائيًا	workflow engine يرسل incremental events	app/agent/workflow.py	tool execution → event stream → UI
Live component rendering	مثل Dash/Plotly/HTML widgets	سيتم دعمها عبر return-type hooks من tools	app/agent/tools.py, Vanna artifact renderer	LLM returns description → tool returns artifact → UI displays it
🔴 القسم الرابع — تقليل التكلفة (Token Optimization)
العنصر	المفهوم	التطبيق داخل مشروعك	الملفات	العلاقة
Dual Outputs (LLM output + UI artifact)	LLM لا يرى البيانات الكاملة؛ الواجهة تعرض الجدول الكامل بدون تكلفة	LLM يحصل على summary فقط: “Query returned 1247 rows” بينما React يعرض الجدول كاملًا	app/agent/db.py, app/agent/llm.py, frontend/pages/Tables.jsx	DB returns full result → UI renders → LLM sees only metadata
Zero-token rendering	الواجهة تتعامل مع البيانات دون إرساله للـ LLM	Vanna components + React pagination	frontend/pages/Tables.jsx, static/js	LLM cost minimized while user sees full results
🟢 القسم الخامس — مميزات التحليل المتقدم (Analytical Stack)
العنصر	المفهوم	التطبيق داخل مشروعك	الملفات	العلاقة
Built for data analysis	تنفيذ SQL + pagination + CSV export	موجود فعليًا داخل: db layer + UI table component	app/agent/db.py, frontend/pages/Tables.jsx	query → db → pagination → UI
Interactive artifacts	رسومات Plotly / HTML widgets	يُطبق عبر tool hooks & result typings	app/agent/tools.py, custom data visualizer	LLM describes → tool generates → UI renders
🛡️ القسم السادس — الإنتاج (Production-Grade Foundations)
العنصر	المفهوم	التطبيق داخل مشروعك	الملفات	العلاقة
Per-user quota management	عدد الطلبات لكل مستخدم	يمكن تفعيله عبر SlowAPI + middleware	app/main.py, security.py	request → throttler → agent
Usage tracking	حفظ كل استعلام لكل مستخدم	logging + audit table	audit.log, app/utils/logger.py	agent → logger → storage
Conversation persistence	تخزين session per user	memory provider + DB	app/agent/memory.py	LLM context → stored per user
Automatic permission enforcement	كل أداة تتحقق قبل التنفيذ	decorators + permission map	app/agent/security.py	tool exec → permission gate
🔧 كيف تعمل المنظومة بالتسلسل؟ (Flow Diagram Explained)

User يكتب طلبًا داخل <vanna-chat>

الطلب يصل إلى FastAPI middleware → يتم استخراج user_id

يدخل الطلب إلى workflow engine داخل app/agent/workflow.py

الـ Agent يحدد نوع المهمة: SQL / API / tool / LLM

Security Layer يتحقق من:

الهوية

الصلاحيات

كوتا المستخدم

Tool Execution Layer:

إذا SQL → يذهب إلى db.py

إذا Metadata → metadata provider

النتائج تعود بشكل:

LLM summary

UI artifact (جداول/Charts/Lineage/HTML)

الواجهة تحدّث الحالة — stateful UI, وليس append-only

الحوار يستمر مع session معزول لكل مستخدم

