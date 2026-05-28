import sqlite3
import matplotlib.pyplot as plt
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db_manager import create_tables

DB_NAME = "usb_forensics.db"

def fetch_risk_data():
    # Ensure database tables exist
    create_tables()
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT risk_score
        FROM evidence_logs
""")
    
    risks = cursor.fetchall()
    conn.close()
    return [risk[0] for risk in risks]

def show_risk_chart():

    risks = fetch_risk_data()

    high = 0
    medium = 0
    low = 0

    for score in risks:
        if score >= 10:
            high += 1
        elif score >= 5:
            medium += 1
        else:
            low += 1
    
    labels = [
        "High Risk",
        "Medium Risk",
        "Low Risk"
    ]

    values = [
        high,
        medium,
        low
    ]

    plt.figure(figsize=(6, 6))

    if sum(values) == 0:
        plt.text(0.5, 0.5, 'No risk data available', 
                ha='center', va='center', fontsize=14)
    else:
        plt.pie(
            values,
            labels=labels,
            autopct='%1.1f%%',
        )

    plt.title(
        "USB Forensics Risk Distribution"
    )

    plt.show()

if __name__ == "__main__":

    show_risk_chart()