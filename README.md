
🎓 Student Data ETL Pipeline
From Messy Excel Sheets to a Clean MySQL Database

Part of my Data Engineering Learning Journey — building real pipelines, solving real data problems.


🚀 The Story Behind This Project
Ever received a dataset that looks like it was filled in by 10 different people on 10 different days?
That's exactly what this project starts with — 500 student records collected from multiple sources, full of typos, inconsistencies, missing values, and chaos. The goal was simple: build a pipeline that takes this mess and turns it into something a database — and a data analyst — can actually use.
This is not a toy project. Every dirty data problem in this dataset is something you'll encounter in a real job — invalid emails, phone numbers with special characters, department names spelled 6 different ways, ages of -5 and 120. The cleaning logic handles all of it.

🔄 Pipeline at a Glance
students.xlsx
      ↓
   EXTRACT          ← Read 500 raw rows from Excel
      ↓
   CLEAN            ← Fix, validate, standardize everything
      ↓
   LOAD             ← Push 480 clean rows into MySQL
      ↓
 SQL REPORTS        ← Answer real business questions

🧹 The Dirty Data Problem
This is where the real learning happens. The raw Excel file had:
Dirty Data TypeExampleFixed ToDuplicate rowsSame student 7 timesRemovedFully empty rowsAll columns blankDroppedInvalid emailsjohn@, @gmail, nodomain→ NULLInvalid phones123, 99999999999999, 98#45→ NULLInconsistent departmentscse, CSE, Cse, Computer Science→ CSEInconsistent citiesHYDERABAD, hyd, Hyderabad → HyderabadFee status chaosPAID, p a i d, Payed→ PaidBad CGPA values-1.5, 13.0→ NULLBad attendance-10, 150→ NULLUnrealistic ages-5, 120→ NULLSpecial chars in namesRahul@#Singh→ Rahul Singh
500 rows in → 480 clean rows out → 0 corrupt records in MySQL

📊 What the Data Tells Us (SQL Reports)
After loading into MySQL, these questions get answered automatically:

🏫 Which department has the most students?
📉 Which students are at risk due to low attendance?
💰 How many students still haven't paid fees?
🏆 Who are the top 10 performers by CGPA?
📅 How have admissions trended year over year?
🔍 How many NULLs remain per column after cleaning?


🛠️ Tech Stack
ToolPurposePythonPipeline logicPandasData extraction and cleaningMySQLClean data storageSQLAlchemyPython-to-MySQL connectionPyMySQLMySQL driverOpenPyXLReading .xlsx files

📁 Project Structure
student_etl/
│
├── students.xlsx        ← raw input (500 rows, intentionally dirty)
├── etl_pipeline.py      ← full ETL pipeline
├── requirements.txt     ← all dependencies
└── README.md

▶️ Run It Yourself
1. Clone the repo
bashgit clone https://github.com/your-username/student-etl-pipeline.git
cd student-etl-pipeline
2. Install dependencies
bashpip install -r requirements.txt
3. Create the MySQL database
sqlCREATE DATABASE students_etl;
4. Update your credentials in etl_pipeline.py
pythonDB_USER     = "root"
DB_PASSWORD = quote_plus("your_password")
DB_NAME     = "students_etl"
5. Run the pipeline
bashpython etl_pipeline.py
6. Watch it go
Extracted 500 rows
Clean rows ready to load: 480
Data loaded into MySQL successfully!

📈 Results
Raw Input Rows        →   500
Fully Empty Dropped   →    10
Duplicates Removed    →     7
Failed Critical Check →     3
─────────────────────────────
Clean Rows Loaded     →   480

💡 What I Actually Learned
This wasn't just about writing code. It taught me how to think like a data engineer:

Never trust raw data — always validate before loading
Regex is your best friend for email and phone validation
Mapping dictionaries are the cleanest way to standardize inconsistent values
ENUM types in MySQL enforce data integrity at the database level
URL-encoding passwords matters when special characters are involved (@ in a password breaks connection strings)
The difference between dropping bad rows vs. nulling bad values — and when to do each


🗺️ My Data Engineering Journey
This project is Part 1 of my hands-on data engineering learning path:
#ProjectSkillsStatus1Student ETL PipelinePython, Pandas, MySQL, Data Cleaning✅ Done2Coming soonAirflow / Pipeline Scheduling🔄 Next3Coming soonCloud Storage (S3 / GCS)⏳ Planned4Coming soonData Warehousing (BigQuery / Snowflake)⏳ Planned5Coming soonReal-time Streaming (Kafka)⏳ Planned

👩‍💻 Author
Yasaswini

Aspiring Data Engineer — learning by building
