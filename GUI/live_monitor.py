import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt5.QtCore import QThread, pyqtSignal

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from forensic.hash_analyzer import generate_sha256
from Risk.risk_engine import calculate_risk
from database.db_manager import insert_log

from datetime import datetime

import time

from Alerts.email_alert import send_email_alert

class EventHandler(FileSystemEventHandler):

    def __init__(self, signal):

        super().__init__()

        self.signal = signal

    def process_event(self, event_type, file_path):
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        sha256_hash = generate_sha256(file_path)

        risk_score, reasons = calculate_risk(file_path)

        reason_text = "; ".join(reasons)

        insert_log(
            timestamp,
            event_type,
            file_path,
            sha256_hash,
            risk_score,
            reason_text
        )

        message = f"""
TIME : {timestamp}
EVENT : {event_type}
FILE : {file_path}
HASH : {sha256_hash}
RISK SCORE : {risk_score}
REASONS : {reason_text}

---------------------------------
"""
        self.signal.emit(message)
        
        if risk_score >= 10:
            send_email_alert(
                file_path,
                risk_score,
                reason_text
            )
    
    def on_created(self, event):

        if not event.is_directory:
            self.process_event(
                "CREATED",
                event.src_path
            )
    
    def on_deleted(self, event):
        
        if not event.is_directory:
            self.process_event(
                "DELETED",
                event.src_path
            )

    def on_modified(self, event):

        if not event.is_directory:
            self.process_event(
                "MODIFIED",
                event.src_path
            )

    def on_moved(self, event):

        if not event.is_directory:
            self.process_event(
                "REMOVED/MOVED",
                f"{event.src_path} -> {event.dest_path}"
            )

class MonitorThread(QThread):

    log_signal = pyqtSignal(str)

    def __init__(self, path):

        super().__init__()

        self.path = path

    def run(self):

        if not os.path.exists(self.path):
            print(f"Error: Path does not exist: {self.path}")
            return

        event_handler = EventHandler(
            self.log_signal
        )

        observer = Observer()

        observer.schedule(
            event_handler,
            self.path,
            recursive=True
        )

        observer.start()

        try:
            while True:
                time.sleep(1)

        except:
            observer.stop()

        observer.join()