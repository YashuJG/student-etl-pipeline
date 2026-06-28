# 🎓 Student Data ETL Pipeline
### From Messy Excel Sheets to a Clean MySQL Database + Analytics Dashboard

![Python](https://img.shields.io/badge/Python-3.12-blue) ![Pandas](https://img.shields.io/badge/Pandas-2.0-green) ![MySQL](https://img.shields.io/badge/MySQL-8.0-orange) ![Excel](https://img.shields.io/badge/Excel-Dashboard-brightgreen)

---

## 📌 Problem Statement

In real organizations, data arrives daily from multiple sources — different people filling forms in different formats. The result is dirty, inconsistent, unreliable data that cannot be used for reporting or decision-making.

This project solves that problem by building an **automated ETL pipeline** that:
- Takes 500 raw, messy student records from Excel
- Applies 10+ data validation and cleaning rules using Python
- Loads only clean, trustworthy records into a MySQL database
- Generates automated SQL reports answering real business questions
- Visualizes insights in an Excel analytics dashboard

> Without this pipeline: wrong data → wrong reports → wrong decisions.
> With this pipeline: clean data → accurate reports → reliable insights.

---

## 🔄 Pipeline Architecture

```
students.xlsx  (500 raw rows)
      ↓
   EXTRACT       ← Read Excel file using Pandas
      ↓
   CLEAN         ← Validate and fix 10+ data quality issues
      ↓
   LOAD          ← Push 480 clean rows into MySQL
      ↓
 SQL REPORTS     ← Answer 8 real business questions
      ↓
EXCEL DASHBOARD  ← Visualize insights with charts + KPIs
```

---

## 🧹 Data Quality Problems Solved

| Dirty Data Problem | Example | How It Was Fixed |
|---|---|---|
| Duplicate rows | Same student 7 times | Removed with drop_duplicates() |
| Fully empty rows | All columns blank | Dropped with dropna(how='all') |
| Invalid emails | john@, @gmail, nodomain | Set to NULL via regex validation |
| Invalid phone numbers | 98#45, 123, 9999999 | Set to NULL, stripped country codes |
| Inconsistent departments | cse, CSE, Cse, Computer Science | Standardized to CSE via mapping |
| Inconsistent cities | HYDERABAD, hyd, Hyderabad | Standardized via city mapping |
| Fee status chaos | PAID, p a i d, Payed | Standardized to Paid/Unpaid/Pending |
| Invalid CGPA | -1.5, 13.0 | Set to NULL (must be 0–10) |
| Invalid attendance | -10, 150 | Set to NULL (must be 0–100) |
| Unrealistic ages | -5, 120 | Set to NULL (must be 15–60) |
| Bad admission year | 1800, 9999 | Set to NULL (must be 2000–2025) |
| Special chars in names | Rahul@#Singh | Cleaned to Rahul Singh via regex |

---

## 📊 Data Quality Report (Pipeline Output)

```
========================================
     DATA QUALITY REPORT
========================================
Total Rows Extracted     :  500
Clean Rows Loaded        :  480
Rows Removed/Fixed       :  20
Data Quality Score       :  96.0%
Nulls in Email           :  61
Nulls in Phone           :  59
Nulls in CGPA            :  46
Nulls in Attendance      :  54
========================================
```

---

## 📈 Excel Analytics Dashboard

> **Add your dashboard screenshot here:**
> Replace this line by dragging your dashboard screenshot into GitHub when editing this README.
> Or use this syntax: `![Dashboard](dashboard_screenshot.png)`
> (Upload your screenshot to the same GitHub folder and name it dashboard_screenshot.png)

### Dashboard Includes:
- **Students Per Department** — Bar chart showing enrollment by department
- **Fee Status Distribution** — Pie chart (Paid 44%, Pending 32%, Unpaid 24%)
- **Average CGPA by Department** — Bar chart showing academic performance
- **KPI Summary Box** — Total Students: 480 | Data Quality Score: 96% | Unpaid Fee Count: 107 | At-Risk Students: 20

---

## 💼 Business Insights Delivered

| Insight | Finding |
|---|---|
| Largest department | EEE — 75 students |
| Best academic department | CSE — Average CGPA 7.93 |
| Fee collection alert | 55.6% students not fully paid (107 Unpaid + 144 Pending) |
| At-risk students | 20 students with attendance below 75% |
| Peak admission year | 2021 — 79 admissions |
| Data quality achieved | 96% clean records after pipeline |

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.12 | Pipeline logic and automation |
| Pandas | Data extraction, cleaning, transformation |
| NumPy | Handling NaN values |
| MySQL 8.0 | Clean data storage |
| SQLAlchemy | Python-to-MySQL connection |
| PyMySQL | MySQL driver |
| OpenPyXL | Reading .xlsx files |
| Excel | Analytics dashboard and visualization |
| Regular Expressions (re) | Email and phone validation |

---

## 📁 Project Structure

```
student_etl/
│
├── et1_pipeline.py          ← Full ETL pipeline (Extract + Clean + Load + Report)
├── students.xlsx            ← Raw input (500 rows, intentionally dirty)
├── student_analysis_dashboard.xlsx  ← Excel dashboard with charts
├── requirements.txt         ← All Python dependencies
└── README.md                ← This file
```

---

## ▶️ How to Run

**1. Clone the repository**
```bash
git clone https://github.com/your-username/student-etl-pipeline.git
cd student-etl-pipeline
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Create MySQL database**
```sql
CREATE DATABASE students_et1;
```

**4. Update your credentials in et1_pipeline.py**
```python
DB_USER     = "root"
DB_PASSWORD = quote_plus("your_password")
DB_NAME     = "students_et1"
```

**5. Run the pipeline**
```bash
python et1_pipeline.py
```

**6. Expected output**
```
Extracted 500 rows
Data Quality Score: 96.0%
Data loaded into MySQL successfully!
[8 SQL reports printed automatically]
```

---

## 📋 SQL Reports Generated

The pipeline automatically runs 8 business reports after loading:

1. Total Students Count
2. Students Per Department
3. Average CGPA Per Department
4. Fee Status Breakdown with Percentages
5. Students With Low Attendance (Below 75%) — At-Risk List
6. Top 10 Students By CGPA
7. Admissions Trend Per Year
8. NULL Count Per Column — Data Quality Audit

---

## 💡 Key Learnings

- Never trust raw data — always validate before loading
- Regex is essential for email and phone validation
- Mapping dictionaries are the cleanest way to standardize inconsistent values
- ENUM types in MySQL enforce data integrity at the database level
- The difference between dropping bad rows vs. nulling bad values — and when to do each
- A Data Quality Score gives stakeholders a single number to measure data health
- URL-encoding passwords matters when special characters are involved

---

## 🗺️ Skills Demonstrated

- ETL Pipeline Design and Implementation
- Data Quality Validation (10+ rules)
- Python Automation with Pandas
- SQL Business Reporting (8 queries)
- Excel Dashboard Creation with Pivot Tables and Charts
- Database Design with MySQL (ENUM types, constraints, auto-increment)
- Error Handling and Defensive Coding
- GitHub Documentation

---

## 👩‍💻 Author

**Yasaswini**
Aspiring Data Engineer — learning by building real pipelines that solve real problems.
