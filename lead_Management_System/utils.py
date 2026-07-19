from datetime import datetime
import sqlite3
from config import Config


# ===============================
# Get Current Date & Time
# ===============================
def current_datetime():
    return datetime.now().strftime("%d-%m-%Y %H:%M:%S")


# ===============================
# Get Database Connection
# ===============================
def get_connection():
    conn = sqlite3.connect(Config.DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# ===============================
# Check Duplicate Mobile Number
# ===============================
def is_duplicate_mobile(mobile):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM leads WHERE mobile=?",
        (mobile,)
    )

    count = cursor.fetchone()[0]

    conn.close()

    return count > 0


# ===============================
# Add Activity Log
# ===============================
def log_activity(lead_id, action, user="System"):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO activity_log
        (lead_id, action, user, timestamp)
        VALUES (?, ?, ?, ?)
    """, (
        lead_id,
        action,
        user,
        current_datetime()
    ))

    conn.commit()
    conn.close()


# ===============================
# Generate Student ID
# ===============================
def generate_student_id():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM leads")

    total = cursor.fetchone()[0]

    conn.close()

    return f"STD{1000 + total}"


# ===============================
# Generate Admission Number
# ===============================
def generate_admission_no():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM leads")

    total = cursor.fetchone()[0]

    conn.close()

    return f"ADM{5000 + total}"


# ===============================
# Validate Mobile Number
# ===============================
def validate_mobile(mobile):

    return mobile.isdigit() and len(mobile) == 10


# ===============================
# Validate Email
# ===============================
def validate_email(email):

    if email == "":
        return True

    return "@" in email and "." in email


# ===============================
# Dashboard Counts
# ===============================
def dashboard_counts():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM leads")
    total_leads = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM leads WHERE status='Pending'"
    )
    pending = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM leads WHERE status='Admission Confirmed'"
    )
    admissions = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM followups WHERE status='Pending'"
    )
    followups = cursor.fetchone()[0]

    conn.close()

    return {
        "total_leads": total_leads,
        "pending_leads": pending,
        "admissions": admissions,
        "today_followups": followups
    }


# ===============================
# Search Leads
# ===============================
def search_leads(keyword):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM leads
        WHERE
        name LIKE ?
        OR mobile LIKE ?
        OR course LIKE ?
        OR city LIKE ?
        OR counsellor LIKE ?
    """, (
        f"%{keyword}%",
        f"%{keyword}%",
        f"%{keyword}%",
        f"%{keyword}%",
        f"%{keyword}%"
    ))

    data = cursor.fetchall()

    conn.close()

    return data