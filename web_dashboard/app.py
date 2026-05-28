import os
import sys
import sqlite3
from pathlib import Path

from flask import Flask, render_template

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from database.db_manager import create_tables, connect_db

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for
)

from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    login_required,
    logout_user
)

app = Flask(__name__)

app.secret_key = "super_secret_key"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

DB_NAME = "usb_forensics.db"

#demo user
USERS = {
    "admin": "admin123"
}

class User(UserMixin):
    
    def __init__(self, username):
        self.id = username

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


def fetch_logs():
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
        ORDER BY timestamp DESC
""")
    logs = cursor.fetchall()
    conn.close()
    return logs

@app.route("/login", methods= ["GET", "POST"])

def login():

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if (
            username in USERS
            and USERS[username] == password
        ):
            user = User(username)
            login_user(user)
            return redirect(url_for("index"))
    return render_template("login.html")

@app.route("/logout")
@login_required

def logout():
    
    logout_user()
    return redirect(url_for("login"))

@app.route("/")
@login_required

def index():
    logs = fetch_logs()
    total_events = len(logs)

    high_risk = len([
        log for log in logs if log[3] >= 10
    ])

    return render_template(
        "index.html",
        logs=logs,
        total_events=total_events,
        high_risk=high_risk
    )

if __name__ == "__main__":
    app.run(
        debug=True
    )