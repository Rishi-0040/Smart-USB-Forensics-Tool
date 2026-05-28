import os
import sys
import sqlite3
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from database.db_manager import create_tables

DB_NAME = BASE_DIR / "usb_forensics.db"

def export_logs_to_json():
    create_tables()

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT
            timestamp,
            event_type,
            file_path,
            sha256_hash,
            risk_score,
            risk_reasons
        FROM evidence_logs
        ORDER BY timestamp ASC
""")
    
    rows = cursor.fetchall()
    conn.close()

    logs = []

    for row in rows:
        logs.append({
            "timestamp": row[0],
            "event_type": row[1],
            "file_path": row[2],
            "sha256_hash": row[3],
            "risk_score": row[4],
            "risk_reasons": row[5]
        })

    with open(
        "usb_forensics_logs.json",
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            logs,
            file,
            indent=4
            )
    
    print(
        "[+] JSON logs exportd successfully!"
    )

if __name__ == "__main__":
    export_logs_to_json()