#Imports & Config
import pandas as pd
import numpy as np
import re
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus

#MySQL connection
DB_USER     = "root"
DB_PASSWORD = quote_plus("your_password")   # encodes @ safely
DB_HOST     = "localhost"
DB_PORT     = "3306"
DB_NAME     = "students_et1"

engine = create_engine(
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

#EXTRACT
def extract():
    df = pd.read_excel("students.xlsx", dtype=str)
    print(f"Extracted {len(df)} rows")
    return df

#CLEAN
def clean(df):

    # Replace blank strings with NaN
    df.replace(r'^\s*$', np.nan, regex=True, inplace=True)

    # Drop fully empty rows
    df.dropna(how='all', inplace=True)

    # Drop duplicates
    df.drop_duplicates(inplace=True)

    # full_name: strip spaces, remove special characters
    df['full_name'] = df['full_name'].str.strip()
    df['full_name'] = df['full_name'].apply(
        lambda x: re.sub(r'[^A-Za-z\s]', '', str(x)).title() if pd.notna(x) else x
    )

    # email: validate format
    def validate_email(val):
        if pd.isnull(val):
            return np.nan
        pattern = r'^[\w.\-+]+@[\w.\-]+\.[a-zA-Z]{2,}$'
        return val.strip() if re.match(pattern, str(val).strip()) else np.nan

    df['email'] = df['email'].apply(validate_email)

    # phone: keep only 10-digit numbers
    def clean_phone(val):
        if pd.isnull(val):
            return np.nan
        digits = re.sub(r'\D', '', str(val))
        if len(digits) == 12 and digits.startswith('91'):
            digits = digits[2:]
        return digits if len(digits) == 10 else np.nan

    df['phone_number'] = df['phone_number'].apply(clean_phone)

    # gender: normalize
    gender_map = {'m': 'Male', 'male': 'Male', 'f': 'Female', 'female': 'Female'}
    df['gender'] = df['gender'].str.strip().str.lower().map(gender_map)

    # age: must be 15-60
    df['age'] = pd.to_numeric(df['age'], errors='coerce')
    df.loc[~df['age'].between(15, 60), 'age'] = np.nan

    # department: standardize all variations
    dept_map = {
        'cse': 'CSE', 'cs': 'CSE', 'computer science': 'CSE', 'c.s.e': 'CSE',
        'ece': 'ECE', 'electronics': 'ECE', 'e.c.e': 'ECE',
        'me': 'ME', 'mechanical': 'ME', 'mech': 'ME',
        'civil': 'Civil', 'civil engineering': 'Civil', 'ce': 'Civil',
        'it': 'IT', 'information technology': 'IT', 'info tech': 'IT',
        'mba': 'MBA', 'business administration': 'MBA',
        'bca': 'BCA', 'b.c.a': 'BCA',
        'eee': 'EEE', 'electrical': 'EEE', 'electrical engineering': 'EEE',
    }
    df['department'] = df['department'].str.strip().str.lower().map(dept_map)

    # city: normalize
    city_map = {
        'hyderabad': 'Hyderabad', 'hyd': 'Hyderabad',
        'mumbai': 'Mumbai',       'bombay': 'Mumbai',
        'delhi': 'Delhi',         'new delhi': 'Delhi',
        'bangalore': 'Bangalore', 'bengaluru': 'Bangalore',
        'chennai': 'Chennai',     'madras': 'Chennai',
        'pune': 'Pune',           'poona': 'Pune',
        'kolkata': 'Kolkata',     'calcutta': 'Kolkata',
        'ahmedabad': 'Ahmedabad', 'jaipur': 'Jaipur', 'lucknow': 'Lucknow',
    }
    df['city'] = df['city'].str.strip().str.lower().map(city_map)

    # cgpa: must be 0-10
    df['cgpa'] = pd.to_numeric(df['cgpa'], errors='coerce')
    df.loc[~df['cgpa'].between(0, 10), 'cgpa'] = np.nan

    # attendance: must be 0-100
    df['attendance_percentage'] = pd.to_numeric(df['attendance_percentage'], errors='coerce')
    df.loc[~df['attendance_percentage'].between(0, 100), 'attendance_percentage'] = np.nan

    # fee_status: normalize
    fee_map = {
        'paid': 'Paid', 'p a i d': 'Paid', 'payed': 'Paid',
        'unpaid': 'Unpaid',
        'pending': 'Pending',
    }
    df['fee_status'] = df['fee_status'].str.strip().str.lower().map(fee_map)

    # Drop rows missing critical fields
    df.dropna(subset=['student_id', 'full_name'], inplace=True)
    df.reset_index(drop=True, inplace=True)

    print(f"Clean rows ready to load: {len(df)}")
    return df

# LOAD into MySQL
def load(df):

    create_table_sql = """
    CREATE TABLE IF NOT EXISTS students (
        id                    INT AUTO_INCREMENT PRIMARY KEY,
        student_id            VARCHAR(20) UNIQUE NOT NULL,
        full_name             VARCHAR(100),
        email                 VARCHAR(100),
        phone_number          VARCHAR(15),
        gender                ENUM('Male', 'Female'),
        age                   INT,
        department            VARCHAR(50),
        city                  VARCHAR(50),
        admission_year        INT,
        cgpa                  DECIMAL(4,2),
        attendance_percentage DECIMAL(5,2),
        fee_status            ENUM('Paid', 'Unpaid', 'Pending'),
        loaded_at             TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """

    with engine.connect() as conn:
        conn.execute(text(create_table_sql))
        conn.commit()

    df.to_sql(
        name='students',
        con=engine,
        if_exists='append',
        index=False,
        method='multi'
    )

    print("Data loaded into MySQL successfully!")

# SQL REPORTS
def run_reports():

    reports = {

        "Total Students": """
            SELECT COUNT(*) AS total_students
            FROM students
        """,

        "Students Per Department": """
            SELECT department, COUNT(*) AS total
            FROM students
            WHERE department IS NOT NULL
            GROUP BY department
            ORDER BY total DESC
        """,

        "Average CGPA Per Department": """
            SELECT department, ROUND(AVG(cgpa), 2) AS avg_cgpa
            FROM students
            WHERE department IS NOT NULL
            GROUP BY department
            ORDER BY avg_cgpa DESC
        """,

        "Fee Status Breakdown": """
            SELECT fee_status, COUNT(*) AS count,
                   ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM students WHERE fee_status IS NOT NULL), 1) AS percentage
            FROM students
            WHERE fee_status IS NOT NULL
            GROUP BY fee_status
        """,

        "Students With Low Attendance (Below 75%)": """
            SELECT student_id, full_name, department, attendance_percentage
            FROM students
            WHERE attendance_percentage < 75
            ORDER BY attendance_percentage ASC
            LIMIT 20
        """,

        "Top 10 Students By CGPA": """
            SELECT student_id, full_name, department, cgpa, attendance_percentage
            FROM students
            ORDER BY cgpa DESC
            LIMIT 10
        """,

        "Admissions Per Year": """
            SELECT admission_year, COUNT(*) AS admissions
            FROM students
            WHERE admission_year IS NOT NULL
            GROUP BY admission_year
            ORDER BY admission_year
        """,

        "NULL Count Per Column (Data Quality Check)": """
            SELECT 'email'                  AS column_name, SUM(email IS NULL)                  AS null_count FROM students
            UNION ALL
            SELECT 'phone_number',                          SUM(phone_number IS NULL)            FROM students
            UNION ALL
            SELECT 'age',                                   SUM(age IS NULL)                     FROM students
            UNION ALL
            SELECT 'cgpa',                                  SUM(cgpa IS NULL)                    FROM students
            UNION ALL
            SELECT 'attendance_percentage',                 SUM(attendance_percentage IS NULL)   FROM students
            UNION ALL
            SELECT 'fee_status',                            SUM(fee_status IS NULL)              FROM students
        """,
    }

    for title, sql in reports.items():
        print(f"\n{'─' * 50}")
        print(f"  {title}")
        print(f"{'─' * 50}")
        df = pd.read_sql(sql, engine)
        print(df.to_string(index=False))

if __name__ == "__main__":
    raw_df   = extract()
    clean_df = clean(raw_df)
    load(clean_df)
    run_reports()