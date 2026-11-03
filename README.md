# 🎮 League of Legends Match Outcome Predictor & Streamlit Dashboard

An end-to-end Machine Learning classification web application that predicts the winning team in high-rank (**High Diamond / Master**) **League of Legends** matches based on the first 10 minutes of telemetry data.

---

## 🇮🇷 مستندات کامل فارسی (Persian Documentation)

### ۱. معرفی و هدف پروژه
این مخزن شامل یک سیستم کامل یادگیری ماشین و داشبورد وب تعاملی برای پیش‌بینی نتیجه مسابقات رنکد بازی **League of Legends** در ۱۰ دقیقه ابتدایی بازی است. پروژه از الگوریتم **درخت تصمیم طبقه‌بندی (`DecisionTreeClassifier`)** بر روی دیتاست رسمی ۹,۸۷۹ مسابقه رنکد بالا (`high_diamond_ranked_10min.csv`) استفاده می‌کند و با دقت **۷۲.۴۷٪** تیم برنده و درصد شانس پیروزی هر تیم را محاسبه می‌نماید.

### ۲. ساختار پوشه و فایل‌های مخزن
```text
lol-match-predictor/
│
├── model.py                        # هسته یادگیری ماشین و آموزش درخت تصمیم
├── app.py                          # وب‌اپلیکیشن و رابط کاربری گیمینگ با Streamlit
├── high_diamond_ranked_10min.csv   # دیتابیس رسمی مسابقات High Diamond لیگ آف لجندز
├── requirements.txt                # لیست کتابخانه‌های مورد نیاز
└── README.md                       # مستندات کامل دو زبانه
```

### ۳. بررسی خط به خط هسته یادگیری ماشین (`model.py`)
1. **فراخوانی کتابخانه‌ها (`Imports`):**
   - `pandas`: خواندن فایل CSV دیتابیس و مدیریت ساختار دیتافریم.
   - `train_test_split`: تقسیم تصادفی مسابقات به دو بخش آموزش (۸۰٪) و تست (۲۰٪).
   - `DecisionTreeClassifier`: الگوریتم درخت تصمیم برای طبقه‌بندی دودویی (برد یا باخت تیم آبی).
   - `accuracy_score`: محاسبه درصد دقت پیش‌بینی‌های مدل در مقایسه با نتایج واقعی.
2. **انتخاب ۱۳ ویژگی کلیدی ۱۰ دقیقه اول (`features`):**
   - `blueFirstBlood`: کسب اولین کیل بازی (First Blood).
   - `blueKills` / `redKills`: تعداد کیل‌های تیم آبی و قرمز.
   - `blueAssists` / `redAssists`: تعداد اسیست‌های هر دو تیم.
   - `blueDragons` / `redDragons`: تعداد اژدهای شکارشده توسط هر تیم.
   - `blueTowersDestroyed` / `redTowersDestroyed`: تعداد برج‌های تخریب‌شده.
   - `blueTotalGold` / `redTotalGold`: مجموع طلای کسب‌شده در ۱۰ دقیقه اول.
   - `blueTotalExperience` / `redTotalExperience`: مجموع امتیاز تجربه (XP) هر تیم.
3. **آموزش و جلوگیری از بیش‌برازش (`Overfitting`):**
   - مدل با پارامتر `max_depth=5` و `random_state=42` پیکربندی شده تا حداکثر ۵ سطح شرطی ایجاد کند و به جای حفظ کردن مسابقات، الگوهای اصلی پیروزی (مانند اختلاف طلا و تجربه) را یاد بگیرد.

### ۴. بررسی خط به خط وب‌اپلیکیشن (`app.py`)
1. **طراحی رابط کاربری گیمینگ (Glassmorphism UI):**
   - استفاده از CSS اختصاصی برای ایجاد پنل‌های شیشه‌ای مات و دکمه‌های نئونی.
2. **اتصال پویا به ماژول مدل (`importlib`):**
   - بارگذاری مستقیم شیء `dt_model`، لیست `features` و دقت `accuracy` از فایل `model.py`.
3. **فرم تعاملی دو ستونه (`st.form`) و محاسبه احتمالات (`predict_proba`):**
   - دریافت آمار تیم آبی و قرمز از طریق اسلایدر و منوهای انتخابی و محاسبه درصد دقیق شانس پیروزی هر تیم با متد `model.predict_proba()`.

---

## 🇬🇧 Complete English Documentation

### 1. Project Overview
This project is a production-ready machine learning web application designed to predict the outcome of competitive **League of Legends** matches from early-game (10-minute) indicators, achieving **72.47% test accuracy** across 9,879 High Diamond matches.

### 2. Line-by-Line Code Breakdown
* **`model.py` (Machine Learning Core):**
  - Loads `high_diamond_ranked_10min.csv` via `pandas`.
  - Extracts 13 early-game combat and objective features (`X`) and sets `blueWins` (`0` or `1`) as the binary target (`y`).
  - Splits the dataset (80% train / 20% test) using `train_test_split(..., random_state=42)`.
  - Trains a regularized `DecisionTreeClassifier(max_depth=5, random_state=42)` and evaluates accuracy via `accuracy_score`.
* **`app.py` (Interactive Streamlit Dashboard):**
  - Configures a wide gaming dashboard with frosted-glass containers (`backdrop-filter: blur(12px)`).
  - Dynamically imports the trained model and feature schema from `model.py`.
  - Captures match telemetry via a 2-column form (`col_blue`, `col_red`) and computes real-time win probabilities using `model.predict_proba()`.

---

## 🚀 How to Run / نحوه اجرا

```bash
pip install -r requirements.txt
streamlit run app.py
```
