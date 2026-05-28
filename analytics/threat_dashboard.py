import os
import sys
import sqlite3
from collections import Counter

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.insert(0, BASE_DIR)

from database.db_manager import create_tables, connect_db

def fetch_statistics():
    create_tables()
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT
            file_path,
            risk_score
        FROM evidence_logs
    """)
    rows = cursor.fetchall()
    conn.close()

    total_events = len(rows)

    high_risk = 0
    medium_risk = 0
    low_risk = 0

    extensions = []

    for file_path,risk in rows:
        #risk classification
        if risk >= 10:
            high_risk += 1
        elif risk >=5:
            medium_risk += 1
        else:
            low_risk += 1
        
        # file extention extraction
        if "." in file_path:
            ext = file_path.split(".")[-1].lower()
            extensions.append(ext)

    extension_counts = Counter(extensions)
    top_extensions = extension_counts.most_common(5)

    return {
        "total_events": total_events,
        "high_risk": high_risk,
        "medium_risk": medium_risk,
        "low_risk": low_risk,
        "top_extensions": top_extensions
    }