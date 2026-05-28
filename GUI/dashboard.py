import sys
import sqlite3
import os

# Add parent directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QTextEdit,
    QLabel,
    QLineEdit
)

from Reports.report_generator import generate_pdf_report
from forensic.timeline import generate_timeline

from GUI.live_monitor import MonitorThread

from GUI.analytics import show_risk_chart

from ml_model.anomaly_detector import detect_anomalies

from forensic.device_history import(
    fetch_device_history
)

from SIEM.log_exporter import(
    export_logs_to_json
)

from analytics.threat_dashboard import(
    fetch_statistics
)

DB_NAME = "usb_forensics.db"

class Dashboard(QWidget):

    def __init__(self):

        super().__init__()

        self.setStyleSheet("""
            QWidget {
                background-color: #121212;
                color: #00FF99;
                font-family: Consolas;
                font-size: 14px;
            }
            QPushButton {
                background-color: #1E1E1E;
                border: 2px solid #00FF99;
                border-radius: 10px;
                padding: 10px;
                font-weight: bold;
            }
                           
            QPushButton:hover {
                background-color: #00FF99;
                color: black;
            }
            QTextEdit {
                background-color: #1A1A1A;
                border: 2px solid #00FF99;
                border-radius: 10px;
                padding: 10px;
            }
            QLineEdit {
                background-color: #1A1A1A;
                border: 2px solid #00FF99;
                border-radius: 8px;
                padding: 8px;
            }
            QLabel {
                color: #00FF99;
            }
        """)

        self.setWindowTitle(
            "Smart USB Forensics Tool"
        )

        self.setGeometry(200, 200, 800, 600)

        self.init_ui()
    
    def init_ui(self):

        layout = QVBoxLayout()

        title = QLabel(
            "USB Activity Forensics Dashboard"
        )

        title.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: #00FF99;
            padding: 15px;
        """)

        layout.addWidget(title)

        #USB Path Input
        self.path_input = QLineEdit()

        self.path_input.setPlaceholderText(
            "Enter USB drive path (e.g., E:\\)"
        )

        layout.addWidget(self.path_input)

        #Start Monitoring Button
        self.monitor_btn = QPushButton(
            "Start Live Monitoring"
        )

        self.monitor_btn.clicked.connect(
            self.start_monitoring
        )
        layout.addWidget(self.monitor_btn)
        

        #Button
        self.timeline_btn = QPushButton(
            "View Timeline"
        )
        self.timeline_btn.clicked.connect(
            self.view_timeline
        )

        layout.addWidget(self.timeline_btn)

        self.highrisk_btn = QPushButton(
            "View High-Risk Events"
        )

        self.highrisk_btn.clicked.connect(
            self.view_high_risk
        )

        layout.addWidget(self.highrisk_btn)

        self.report_btn = QPushButton(
            "Generate PDF Report"
        )

        self.report_btn.clicked.connect(
            self.generate_report
        )

        layout.addWidget(self.report_btn)

        #Log Area
        self.log_area = QTextEdit()

        self.log_area.append("""

        =====================================
             SMART USB FORENSICS MONITOR
        =====================================
                             
        [ SYSTEM STATUS ]
        ✔ Threat Detection Active
        ✔ Evidence Logging Enabled
        ✔ Risk Engine Running
        ✔ Timeline Reconstruction Ready

        Waiting For Monitoring...
        """)

        self.log_area.setReadOnly(True)

        layout.addWidget(self.log_area)

        self.setLayout(layout)

        self.analytics_btn = QPushButton(
            "Show Risk Analytics"
        )

        self.analytics_btn.clicked.connect(
            self.show_analytics
        )

        layout.addWidget(self.analytics_btn)

        self.ai_btn = QPushButton(
            "Run AI Threat Detection"
        )

        self.ai_btn.clicked.connect(
            self.run_ai_detection
        )

        layout.addWidget(self.ai_btn)

        self.device_btn = QPushButton(
            "View USB Device History"
        )

        self.device_btn.clicked.connect(
            self.view_device_history
        )

        layout.addWidget(self.device_btn)

        self.siem_btn = QPushButton(
            "Export Logs for SIEM"
        )
        self.siem_btn.clicked.connect(
            self.export_siem_logs
        )
        layout.addWidget(self.siem_btn)

        self.threat_btn = QPushButton(
            "Threat Intelligence Dashboard"
        )
        self.threat_btn.clicked.connect(
            self.show_threat_dashboard
        )
        layout.addWidget(self.threat_btn)

    def view_timeline(self):

        logs = generate_timeline()

        self.log_area.clear()

        for log in logs:

            timestamp, event, file_path, risk, reason = log

            self.log_area.append(
                f"""
TIME: {timestamp}
EVENT: {event}
FILE: {file_path}
RISK: {risk}
REASON: {reason}

----------------------------------
"""
            )
    def view_high_risk(self):

        logs = generate_timeline(
            high_risk_only=True
        )

        self.log_area.clear()

        for log in logs:

            timestamp, event, file_path, risk, reason = log

            self.log_area.append(
                f"""
🚨 HIGH RISK EVENT

TIME: {timestamp}
EVENT: {event}
FILE: {file_path}
RISK: {risk}
REASON: {reason}

----------------------------------
"""
            )
            
    def generate_report(self):

        generate_pdf_report()

        self.log_area.append(
            "\n[+] PDF Report Generated Successfully!\n"
        )
    
    def start_monitoring(self):

        path = self.path_input.text()

        if not path:
            self.log_area.append(
                "[-] Please enter a valid USB drive path.\n"
            )
            return
        
        self.monitor_thread = MonitorThread(path)

        self.monitor_thread.log_signal.connect(
            self.update_log
        )

        self.monitor_thread.start()

        self.log_area.append(
            f"[+] Live monitoring started on: {path}\n"
        )

    def update_log(self, message):

        self.log_area.append(message)

    def show_analytics(self):
        show_risk_chart()

    def run_ai_detection(self):

        self.log_area.append(
            "\n[+] Running AI Threat Analysis...\n"
        )

        import io
        import sys

        captured_output = io.StringIO()

        sys.stdout = captured_output

        detect_anomalies()

        sys.stdout = sys.__stdout__

        output = captured_output.getvalue()

        self.log_area.append(output)

    def view_device_history(self):

        devices = fetch_device_history()
        self.log_area.clear()
        self.log_area.append("""
========================================
          USB DEVICE HISTORY
========================================
""")
        for device in devices:
            timestamp, name, venodor, product, trusted = device

            status = (
            "TRUSTED ✅"
            if trusted
            else
            "UNKNOWN ⚠️"
            )

            self.log_area.append(
                f"""
TIME       :{timestamp}

DEVICE     :{name}

VENDOR ID  :{venodor}

PRODUCT ID :{product}

STATUS     :{status}

--------------------------------------
""")
    
    def export_siem_logs(self):
        export_logs_to_json()
        self.log_area.append(
            "\n[+] SIEM JSON Export Ready\n"
        )

    def show_threat_dashboard(self):
        stats = fetch_statistics()
        self.log_area.clear()
        self.log_area.append("""
======================================
    THREAT INTELLIGENCE DASHBOARD
======================================
""")
        self.log_area.append(
            f"""
📊 TOTAL EVENTS:
{stats['total_events']}

🚨 HIGH RISK EVENTS:
{stats['high_risk']}

⚠️ MEDIUM RISK EVENTS:
{stats['medium_risk']}

🟢 LOW RISK EVENTS:
{stats['low_risk']}
"""
    )
        self.log_area.append("""
======================================
     MOST DETECTED FILE EXTENSION
======================================                           
""")
        for ext, count in stats['top_extensions']:
            self.log_area.append(
                f"""
📁 .{ext} → {count} detections
"""
            )
    
if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = Dashboard()

    window.show()

    sys.exit(app.exec_())