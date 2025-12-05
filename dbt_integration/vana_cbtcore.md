فيما يلي **وثيقة رسمية ومنسقة** تشرح **دور dbt Core في تحسين أداء ودقة Vanna 2**، إضافة إلى **أفضل طرق التكامل بينهما**.
الوثيقة مكتوبة بأسلوب احترافي مباشر، جاهزة للاستخدام كمرجع داخلي أو تصميم معماري.

---

# **وثيقة: دور dbt Core في تحسين أداء ودقة Vanna 2 وآلية التكامل المثلى**

## **1. مقدمة**

تعتمد Vanna 2 على فهم بنية البيانات (Data Structure) والفهم الدلالي (Semantic Understanding) لتوليد SQL دقيق والإجابة عن الأسئلة التحليلية.
ومع أن Vanna قادرة على العمل مباشرة مع قواعد البيانات، إلا أن مستوى دقتها يتأثر بمستوى “وضوح” و”تنظيم” البيانات.

هنا يظهر دور dbt Core.
فـ dbt Core لا يُستخدم فقط كأداة ELT، بل يمكن تشغيله **بدون تنفيذ أي تحويلات** ليعمل كطبقة دلالية (Semantic Layer) تنظّم البيانات وتقدم تعريفات واضحة للبيانات التي تعتمد عليها Vanna.

---

# **2. الدور الفعلي لـ dbt Core في تعزيز قدرات Vanna 2**

## **2.1 إضافة طبقة معنى (Semantic Layer)**

توفر dbt إمكانيات توثيق (Documentation) ووصف للعلاقات والحقول، مما يسمح لـ Vanna بفهم:

* القصد من كل جدول
* دور كل عمود
* المعاني التجارية (Business Semantics)
* العلاقات بين الجداول
* المقاييس المحسوبة (Metrics)

هذا السياق الدلالي يساعد Vanna في:

* توليد SQL أدق
* تقليل الأخطاء في الـ JOIN
* تفسير الأسئلة بشكل منطقي
* فهم مصطلحات المستخدم التجارية
* اختيار الجداول المناسبة تلقائيًا

---

## **2.2 تنظيم البيانات في طبقات Models واضحة**

حتى لو لم تستخدم dbt للتحويلات، يمكنك تنظيم Oracle عبر dbt إلى طبقات:

* **staging**
* **intermediate**
* **marts (analytics)**

Vanna حين ترى هذا التنظيم تصبح أكثر دقة لأنها تتعامل مع:

* جداول مفهومة
* أعمدة موثقة
* نماذج مصممة لغرض التحليل

وهذا يلغي مشكلة “الجداول الخام” التي تشوّش على نماذج الذكاء الاصطناعي.

---

## **2.3 توفير Documentation غني يساعد Vanna على التعلم**

وصف الأعمدة في dbt مثل:

```yaml
columns:
  - name: amount
    description: "Monetary value of the transaction in SAR"
```

يوفّر لـ Vanna:

* معرفة سياق العمود
* معرفة نوعه الوظيفي
* القدرة على تفسير أسئلة المستخدم التي تتعلق بالأعمال
* تحسين فهم اللغة الطبيعية (NLU)

كلما كان الوصف أدق، زادت دقة SQL الذي تولّده Vanna.

---

## **2.4 توفير Metrics موحّدة Shared Metrics**

dbt يوفر ميزة “metrics layer”، مثل:

```yaml
metrics:
  - name: total_revenue
    type: sum
    expr: amount
```

عند دمجها مع Vanna تحصل على:

* مقاييس موحدة
* إجابات دقيقة حتى لو اختلفت صياغة السؤال
* فهم تلقائي للقياسات التجارية
* صياغة SQL بالاعتماد على تعريف موثّق وليس تخمين AI

---

## **2.5 توفير علاقات بين الجداول Relationships**

عندما تصف العلاقات في dbt:

```yaml
relationships:
  - name: customer_id
    description: "Foreign key to customers table"
```

فإن Vanna تصبح قادرة على:

* توليد JOIN الصحيح تلقائيًا
* تفهّم العلاقة بين الجداول
* تجنب الأخطاء الشائعة في الربط

---

## **2.6 بدون صلاحيات خطرة**

في وضع “Documentation-Only Mode”:

* لا يحتاج dbt إلى CREATE أو ALTER
* لا يغيّر Oracle
* لا ينفذ أي SQL ضار
* يحتاج فقط SELECT

وبالتالي فهو آمن تمامًا في بيئة إنتاجية.

---

# **3. كيف يستخدم Vanna محتوى dbt Core؟**

Vanna 2 يستخدم metadata الصادر من dbt عبر:

1. قراءة ملفات YAML الخاصة بالتعريفات
2. قراءة documentation المولدة عبر `dbt docs generate`
3. دمج المعلومات في نموذج فهم البيانات الداخلي
4. استخدام المصطلحات في تفسير اللغة الطبيعية (NLU)
5. استخدام العلاقات والـ metrics في تحسين SQL Generation

**النتيجة:**
SQL أكثر دقة، وتحليل أكثر فهمًا للمنطق التجاري.

---

# **4. التكامل الأمثل بين dbt Core و Vanna 2**

## **4.1 الخطوات العملية للتكامل**

### **الخطوة 1: إنشاء مشروع dbt Core**

```bash
dbt init oracle_semantics
```

### **الخطوة 2: تعريف الجداول Models دون أي تحويلات**

```yaml
models:
  - name: transactions
    description: "Financial transactions table"
```

### **الخطوة 3: إضافة وصف الأعمدة**

```yaml
columns:
  - name: amount
    description: "Transaction amount"
```

### **الخطوة 4: إضافة relationships**

```yaml
relationships:
  - name: cust_id
    description: "Link to customers table"
```

### **الخطوة 5: تعريف semantic metrics**

```yaml
metrics:
  - name: total_amount
    expr: sum(amount)
```

### **الخطوة 6: توليد docs**

```bash
dbt docs generate
```

### **الخطوة 7: قراءة Vanna لهذه المعلومات**

تقوم Vanna تلقائيًا بتحميل metadata من مجلد dbt أو من API إذا وُجد.

---

# **5. فوائد التكامل من منظور الأداء والدقة**

| الفائدة            | التأثير على Vanna               |
| ------------------ | ------------------------------- |
| توثيق الأعمدة      | تحسين فهم معنى الحقول           |
| نماذج منظمة        | تخفيض الأخطاء في SQL            |
| علاقات بين الجداول | JOIN دقيق وسليم                 |
| Layer للمقاييس     | فهم الأسئلة التجارية            |
| Semantic Layer     | تفسير الأسئلة بشكل أقرب للإنسان |
| وصف الجداول        | اختيار الجدول الأنسب للسؤال     |
| تخفيض الغموض       | تقليل التناقضات في النتائج      |

---

# **6. الخلاصة التنفيذية**

## **dbt Core يلعب الدور التالي:**

* توفير طبقة معنى منضبطة
* تعريفات لغوية منظمة
* توثيق شامل يفهمه الذكاء الاصطناعي
* بناء semantic models لتسهيل التحليل
* تنسيق البيانات بشكل يسهل على Vanna قراءته
* بدون المساس بقاعدة البيانات
* وبدون صلاحيات خطرة

## **وبالتالي:**

> **dbt Core يزيد من ذكاء Vanna—not لأنه ينفّذ SQL، بل لأنه يزودها بمعرفة منظمة مسبقًا.**

---
فيما يلي **وثيقة تدريب Vanna على dbt Metadata** مكتوبة بأسلوب رسمي احترافي، جاهزة للاعتماد كمرجع فني أو مستند تصميم داخلي.
الوثيقة تشرح **آلية تدريب Vanna 2 على بيانات dbt** لتحسين الفهم الدلالي ودقة توليد SQL.

---

# **وثيقة: تدريب Vanna على dbt Metadata**

## **1. المقدّمة**

تعتمد Vanna 2 على نموذج فهم لغوي (NLU) قادر على تفسير أسئلة المستخدم وتحويلها إلى SQL.
ولتحقيق دقة عالية، تحتاج Vanna إلى معرفة مسبقة عن:

* الجداول
* الأعمدة
* العلاقات
* التعريفات التجارية
* المقاييس (metrics)
* أسماء الكيانات
* قواعد العمل (business logic)

هذه المعرفة لا يمكن الحصول عليها من Oracle وحده.
لذلك تُستخدم **dbt Core** كمصدر metadata غني ودلالي يقوم Vanna بقراءته لتدريب طبقة الذكاء الاصطناعي على فهم البيانات بشكل صحيح.

---

# **2. الهدف من تدريب Vanna بواسطة dbt**

يسمح تدريب Vanna على dbt بتحسين قدراتها في:

### **2.1 الفهم الدلالي (Semantic understanding)**

من خلال قراءة:

* descriptions
* semantic models
* YAML structure
* metrics
* relationships

---

### **2.2 تحسين توليد SQL**

Vanna تصبح قادرة على:

* اختيار الجداول المناسبة
* استخدام الأعمدة الصحيحة
* بناء JOINs بدقة
* فهم المقاييس التجارية
* التعامل مع المصطلحات غير الموجودة في قاعدة البيانات مباشرة

---

### **2.3 تفسير اللغة الطبيعية**

عند سؤال المستخدم:

> "Give me total revenue by customer."

فإن Vanna تبحث في **dbt metrics** قبل محاولة الاستنتاج من القواعد.

---

# **3. ما هو Metadata الذي تستفيد منه Vanna من dbt؟**

تقرأ Vanna الأنواع التالية من metadata:

| نوع البيانات        | مصدرها في dbt       | تأثيرها على Vanna                 |
| ------------------- | ------------------- | --------------------------------- |
| Documentation       | YAML docs           | فهم وصف الجداول والأعمدة          |
| Semantic Models     | semantic_models.yml | فهم الكيانات والمقاييس            |
| Metrics             | metrics.yml         | بناء SQL معتمد على تعريفات تجارية |
| Relationships       | model relationships | معرفة JOINs المناسبة              |
| Naming conventions  | directory structure | تفضيل الجداول “النظيفة”           |
| Column descriptions | models YAML         | الفهم الدلالي للأعمدة             |
| Table purpose       | model description   | تحديد السياق وتحسين الإجابات      |

---

# **4. المتطلبات الفنية لتدريب Vanna على dbt**

## **4.1 التشغيل في وضع Documentation-Only Mode**

لا يتطلب dbt صلاحيات CREATE أو ALTER.
الصلاحيات المطلوبة:

```
SELECT on the target schema
```

---

## **4.2 تشغيل dbt Metadata Generation**

بعد إعداد المشروع:

```bash
dbt docs generate
```

ينتج:

* manifest.json
* catalog.json
* schema.yml
* metadata عن جميع النماذج

هذه هي الملفات التي يستخدمها Vanna.

---

# **5. خطوات التكامل العملي بين dbt و Vanna**

## **الخطوة 1: إعداد مشروع dbt**

مثال:

```bash
dbt init oracle_semantics
```

---

## **الخطوة 2: إضافة وثائق الأعمدة والجداول**

ملف YAML:

```yaml
version: 2
models:
  - name: transactions
    description: "Customer financial transactions"
    columns:
      - name: amount
        description: "Transaction amount in SAR"
      - name: txn_date
        description: "Date of transaction"
```

---

## **الخطوة 3: تعريف semantic models**

```yaml
semantic_models:
  - name: transactions_sem
    model: ref('transactions')
    measures:
      - name: total_amount
        expr: sum(amount)
      - name: txn_count
        expr: count(txn_id)
```

---

## **الخطوة 4: بناء وثائق dbt**

```bash
dbt docs generate
```

---

## **الخطوة 5: تدريب Vanna على dbt metadata**

### **طريقة 1: via Python API**

```python
from vanna.remote import VannaDefault
vn = VannaDefault(model="oracle-vanna")

vn.train(dbt_manifest_path='target/manifest.json')
vn.train(dbt_catalog_path='target/catalog.json')
vn.train(dbt_metadata_path='models/')
```

---

### **طريقة 2: عبر Folder ingestion**

ضع كل metadata في مجلد:

```
/dbt_metadata
  - manifest.json
  - catalog.json
  - sources.yml
  - models/*.yml
```

ثم:

```python
vn.train_folder("dbt_metadata")
```

---

# **6. كيف تستفيد Vanna بعد التدريب؟**

## **6.1 SQL أدق**

قبل التدريب:
Vanna قد تولد SQL يعتمد على guesswork.

بعد التدريب:
SQL يستند إلى:

* descriptions
* business definitions
* semantic logic
* metrics المعرّفة مسبقاً

---

## **6.2 فهم لغة الأعمال مباشرة**

سؤال المستخدم:

> "Show me the total transactional volume per customer this month"

Vanna تبحث أولاً في:

* metrics
* semantic models
* descriptions
* relationships

ثم تولد SQL مطابقًا للمنطق التجاري.

---

## **6.3 تحسين join logic**

عند وجود:

```yaml
relationships:
  - name: customer_id
    description: "Foreign key to customers table"
```

تقوم Vanna تلقائيًا بـ:

```sql
JOIN customers ON transactions.customer_id = customers.id
```

---

# **7. أفضل ممارسات تدريب Vanna على dbt Metadata**

| الممارسة                 | الهدف                     |
| ------------------------ | ------------------------- |
| كتابة descriptions واضحة | رفع الفهم الدلالي         |
| استخدام semantic models  | توفير منطق تجاري جاهز     |
| تعريف metrics            | الإجابات تصبح معيارية     |
| تجزئة النماذج إلى طبقات  | تحسين اختيار الجداول      |
| توثيق العلاقات           | تحسين الـ JOIN            |
| تحديث metadata باستمرار  | تحسين دقة Vanna عبر الزمن |

---

# **8. الخلاصة التنفيذية**

## **dbt Core يعمل بمثابة “طبقة معنى” أساسية تجعل Vanna تفهم البيانات وليس فقط تقرأها.**

وبالاعتماد على:

* documentation
* semantic models
* metrics
* relationships

تتحول Vanna من مجرد "مولد SQL" إلى "مساعد ذكي يفهم الأعمال".

---

# **9. جاهزية التنفيذ**

