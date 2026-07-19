import sqlite3
from config import Config


def get_connection():
    conn = sqlite3.connect(Config.DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():

    conn = get_connection()
    cursor = conn.cursor()

    # -----------------------------
    # Lead Table
    # -----------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS leads(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        mobile TEXT UNIQUE NOT NULL,
        email TEXT,
        course TEXT,
        city TEXT,
        source TEXT,
        status TEXT DEFAULT 'New Enquiry',
        counsellor TEXT DEFAULT 'Not Assigned',
        created_date TEXT,
        updated_date TEXT
    )
    """)

    # -----------------------------
    # Follow-up Table
    # -----------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS followups(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        lead_id INTEGER,
        followup_date TEXT,
        followup_time TEXT,
        remarks TEXT,
        status TEXT,
        created_by TEXT,
        FOREIGN KEY(lead_id) REFERENCES leads(id)
    )
    """)

    # -----------------------------
    # Activity Log Table
    # -----------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS activity_log(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        lead_id INTEGER,
        action TEXT,
        user TEXT,
        timestamp TEXT,
        FOREIGN KEY(lead_id) REFERENCES leads(id)
    )
    """)

    conn.commit()
    conn.close()


# ==========================
# Lead CRUD Functions
# ==========================

def add_lead(name, mobile, email, course, city, source,
             status, counsellor, created_date):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO leads
    (name,mobile,email,course,city,source,status,counsellor,created_date)
    VALUES (?,?,?,?,?,?,?,?,?)
    """,
    (name, mobile, email, course, city,
     source, status, counsellor, created_date))

    conn.commit()
    conn.close()


def get_all_leads():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM leads
    ORDER BY id DESC
    """)

    data = cursor.fetchall()

    conn.close()

    return data


def get_lead(lead_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM leads
    WHERE id=?
    """, (lead_id,))

    data = cursor.fetchone()

    conn.close()

    return data


def update_status(lead_id, status):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE leads
    SET status=?
    WHERE id=?
    """, (status, lead_id))

    conn.commit()
    conn.close()


# ==========================
# Follow-up Functions
# ==========================

def add_followup(
        lead_id,
        followup_date,
        followup_time,
        remarks,
        status,
        created_by):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO followups
    (lead_id,followup_date,followup_time,
     remarks,status,created_by)
    VALUES (?,?,?,?,?,?)
    """,
    (
        lead_id,
        followup_date,
        followup_time,
        remarks,
        status,
        created_by
    ))

    conn.commit()
    conn.close()


def get_followups():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM followups
    ORDER BY id DESC
    """)

    data = cursor.fetchall()

    conn.close()

    return data


# ==========================
# Activity Log
# ==========================

def add_activity(lead_id, action, user, timestamp):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO activity_log
    (lead_id,action,user,timestamp)
    VALUES (?,?,?,?)
    """,
    (lead_id, action, user, timestamp))

    conn.commit()
    conn.close()


def get_activity():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM activity_log
    ORDER BY id DESC
    """)

    data = cursor.fetchall()

    conn.close()

    return data


# ==========================
# Dashboard Functions
# ==========================

def total_leads():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM leads")

    total = cursor.fetchone()[0]

    conn.close()

    return total


def pending_leads():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT COUNT(*)
    FROM leads
    WHERE status='Pending'
    """)

    total = cursor.fetchone()[0]

    conn.close()

    return total


def admissions():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT COUNT(*)
    FROM leads
    WHERE status='Admission Confirmed'
    """)

    total = cursor.fetchone()[0]

    conn.close()

    return total

# ==========================
# Get Lead By ID
# ==========================
def get_lead_by_id(lead_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM leads WHERE id=?",
        (lead_id,)
    )

    lead = cursor.fetchone()

    conn.close()

    return lead


# ==========================
# Update Lead
# ==========================
def update_lead(
    lead_id,
    name,
    mobile,
    email,
    course,
    city,
    source,
    status,
    counsellor
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE leads
        SET
        name=?,
        mobile=?,
        email=?,
        course=?,
        city=?,
        source=?,
        status=?,
        counsellor=?
        WHERE id=?
    """,
    (
        name,
        mobile,
        email,
        course,
        city,
        source,
        status,
        counsellor,
        lead_id
    ))

    conn.commit()
    conn.close()

# ==========================
# Delete Lead
# ==========================

def delete_lead(lead_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM leads WHERE id=?",
        (lead_id,)
    )

    conn.commit()
    conn.close()

# ==========================
# Get All Follow-ups
# ==========================

def get_all_followups():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            followups.id,
            leads.name,
            followups.followup_date,
            followups.followup_time,
            followups.remarks,
            followups.status,
            followups.created_by
        FROM followups
        INNER JOIN leads
        ON followups.lead_id = leads.id
        ORDER BY followups.id DESC
    """)

    data = cursor.fetchall()

    conn.close()

    return data

# ==========================
# Get Follow-up By ID
# ==========================

def get_followup_by_id(followup_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM followups WHERE id=?",
        (followup_id,)
    )

    data = cursor.fetchone()

    conn.close()

    return data


# ==========================
# Update Follow-up
# ==========================

def update_followup(
    followup_id,
    followup_date,
    followup_time,
    remarks,
    status
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE followups
        SET
            followup_date=?,
            followup_time=?,
            remarks=?,
            status=?
        WHERE id=?
    """,
    (
        followup_date,
        followup_time,
        remarks,
        status,
        followup_id
    ))

    conn.commit()
    conn.close()


# ==========================
# Delete Follow-up
# ==========================

def delete_followup(followup_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM followups WHERE id=?",
        (followup_id,)
    )

    conn.commit()
    conn.close()


# ==========================
# Update Follow-up Status
# ==========================

def update_followup_status(followup_id, status):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE followups
        SET status=?
        WHERE id=?
    """,
    (
        status,
        followup_id
    ))

    conn.commit()
    conn.close()