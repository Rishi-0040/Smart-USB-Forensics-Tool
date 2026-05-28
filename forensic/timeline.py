import sqlite3
import sys
import os
import csv

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db_manager import create_tables

DB_NAME = "usb_forensics.db"

def get_severity(risk_score):

    if risk_score >= 10:
        return "HIGH"
    elif risk_score >= 5:
        return "MEDIUM"
    else:
        return "LOW"


def generate_timeline(high_risk_only=False):
    # Ensure tables are created
    create_tables()
    
    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    if high_risk_only:

        cursor.execute("""
            SELECT
                timestamp,
                event_type,
                file_path,
                risk_score,
                risk_reasons
            FROM evidence_logs
            ORDER BY timestamp ASC
        """)
    else:
        cursor.execute("""
            SELECT
                timestamp,
                event_type,
                file_path,
                risk_score,
                risk_reasons
            FROM evidence_logs
            ORDER BY timestamp ASC
        """)

    logs = cursor.fetchall()

    conn.close()

    return logs


def display_timeline(high_risk_only=False):

    logs = generate_timeline(high_risk_only)

    print("\n========== FORENSIC TIMELINE ==========\n")

    for log in logs:

        timestamp, event, file_path, risk, reason = log

        print(f"TIME   : {timestamp}")
        print(f"EVENT  : {event}")
        print(f"FILE   : {file_path}")
        print(f"RISK   : {risk}")
        print(f"REASON : {reason}")

        print("--------------------------------------")

def export_csv(logs):

    with open("forensic_timeline.csv", "w", newline="",encoding="utf-8") as file:

        writer = csv.writer(file)

        writer.writerow([
            "Timestamp",
            "Event Type",
            "File Path",
            "Risk Score",
            "Severity",
            "Risk Reasons"
        ])

        for log in logs:

            timestamp, event, file_path, risk, reason = log

            severity = get_severity(risk)

            writer.writerow([
                timestamp,
                event,
                file_path,
                risk,
                severity,
                reason
            ])

        print("\n[+] CSV Report Exported Successfully!")
        print("[+] File: forensic_timeline.csv")

if __name__ == "__main__":

    print("""
1. View Complete Timeline
2. View High-Risk Events Only
3. Export Timeline to CSV
""")
    
    choice = input("Enter your choice: ")

    if choice == "1":
        display_timeline()
    elif choice == "2":
        display_timeline(high_risk_only=True)
    elif choice == "3":
        logs = generate_timeline()
        export_csv(logs)
    else:
        print("Invalid choice.")