import sqlite3
import sys
import os

from reportlab.platypus import(
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db_manager import create_tables

DB_NAME = "usb_forensics.db"

def fetch_logs():
    # Ensure database tables exist
    create_tables()
    
    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

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

def get_severity(score):

    if score >= 10:
        return "HIGH"
    elif score >= 5:
        return "MEDIUM"
    else:
        return "LOW"

def generate_pdf_report():

    logs = fetch_logs()

    pdf = SimpleDocTemplate(
        "Forensics_Report.pdf"
    )
    styles = getSampleStyleSheet()
    elements = []

    #title
    title = Paragraph("USB Forensics Investigation Report",
                      styles['Title']
    )
    elements.append(title)
    elements.append(Spacer(1, 20))

    #Table Heading
    data = [[
        "Timestamp",
        "Event Type",
        "File Path",
        "Risk Score",
        "Risk Reason",
        "Severity"
    ]]

    #Table Data
    for log in logs:
        timestamp, event_type, file_path, risk_score, risk_reasons = log
        severity = get_severity(risk_score)
        data.append([
            timestamp,
            event_type,
            file_path,
            str(risk_score),
            risk_reasons,
            severity
        ])

    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ]))
    elements.append(table)

    elements.append(Spacer(1, 20))

    #Summary section
    total_events = len(logs)
    high_risk = len([
        log for log in logs if log [3] >= 10
    ])

    medium_risk = len([
        log for log in logs if 5 <= log[3] < 10
    ])

    low_risk = len([
        log for log in logs if log[3] < 5
    ])

    summary = f"""
    <b>Total Events:</b> {total_events}<br/>
    <b>High Risk Events:</b> {high_risk}<br/>
    <b>Medium Risk Events:</b> {medium_risk}<br/>
    <b>Low Risk Events:</b> {low_risk}<br/>
    """
    summary_paragraph = Paragraph(
        summary,
        styles['BodyText']
    )

    elements.append(summary_paragraph)
    pdf.build(elements)

    print("\n[+] PDF Report Generated Successfully!")
    print("[+] File: Forensics_Report.pdf")

if __name__ == "__main__":
    generate_pdf_report()