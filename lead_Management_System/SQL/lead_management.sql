CREATE TABLE leads(
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
);

CREATE TABLE followups(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    lead_id INTEGER,
    followup_date TEXT,
    followup_time TEXT,
    remarks TEXT,
    status TEXT,
    created_by TEXT,
    FOREIGN KEY(lead_id) REFERENCES leads(id)
);

CREATE TABLE activity_log(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    lead_id INTEGER,
    action TEXT,
    user TEXT,
    timestamp TEXT,
    FOREIGN KEY(lead_id) REFERENCES leads(id)
);
ALTER TABLE followup
ADD status VARCHAR(20) DEFAULT 'Pending';