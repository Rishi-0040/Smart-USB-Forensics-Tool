import sqlite3
import pandas as pd
import sys
import os

from sklearn.ensemble import IsolationForest

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db_manager import create_tables

DB_NAME = "usb_forensics.db"

def load_data():
    # Ensure database tables exist
    create_tables()
    
    conn = sqlite3.connect(DB_NAME)

    query = """
        SELECT risk_score
        FROM evidence_logs
    """

    df = pd.read_sql_query(query, conn)

    conn.close()
    return df

def train_model(df):
    
    model = IsolationForest(
        contamination=0.2,
        random_state=42
    )

    model.fit(df)
    return model

def detect_anomalies():
    
    df = load_data()

    if df.empty:
        print("No Forensic Data Available.")
        return
    
    model = train_model(df)

    df['anomaly'] = model.predict(df)

    print("\n========== AI THREAT ANALYSIS ==========\n")

    for index, row in df.iterrows():
        risk = row['risk_score']
        anomaly = row['anomaly']

        if anomaly == -1:
            print(
                f"🚨 Suspicious Activity Detected "
                f"(Risk Score: {risk})"
            )
        else:
            print(
                f"✔ Normal Activity "
                f"(Risk Score: {risk})"
            )

if __name__ == "__main__":
    detect_anomalies()