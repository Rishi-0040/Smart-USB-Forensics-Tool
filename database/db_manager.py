import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_NAME = os.path.join(BASE_DIR, "usb_forensics.db")

def connect_db():
    return sqlite3.connect(DB_NAME)

def create_tables():

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS evidence_logs(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            event_type TEXT,
            file_path TEXT,
            sha256_hash TEXT,
            risk_score INTEGER,
            risk_reasons TEXT
        )
    """)

    # Add missing columns if they don't exist
    cursor.execute("PRAGMA table_info(evidence_logs)")
    columns = [column[1] for column in cursor.fetchall()]
    
    if "risk_score" not in columns:
        cursor.execute("ALTER TABLE evidence_logs ADD COLUMN risk_score INTEGER")
    
    if "risk_reasons" not in columns:
        cursor.execute("ALTER TABLE evidence_logs ADD COLUMN risk_reasons TEXT")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usb_devices(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            device_name TEXT,
            device_id TEXT,
            vendor_id TEXT,
            product_id TEXT,
            trusted INTEGER DEFAULT 0
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS device_connections(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            device_name TEXT,
            vendor_id TEXT,
            product_id TEXT,
            is_trusted INTEGER DEFAULT 0
        )
    """)

    conn.commit()
    conn.close()

def insert_log(timestamp,
               event_type,
               file_path,
               sha256_hash,
               risk_score,
               risk_reasons):

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO evidence_logs
        (
            timestamp,
            event_type,
            file_path,
            sha256_hash,
            risk_score,
            risk_reasons
        )
        VALUES (?, ?, ?, ?, ?, ?)
     """, (timestamp,
           event_type,
           file_path,
           sha256_hash,
           risk_score,
           risk_reasons))
    
    conn.commit()
    conn.close()