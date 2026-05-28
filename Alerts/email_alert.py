import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SENDER_EMAIL = "your_email@gmail.com"
SENDER_PASSWORD = "your_app_password"

RECEIVER_EMAIL = "receiver@gmail.com"

def send_email_alert(
        file_path,
        risk_score,
        reason
):
    subject = "🚨 HIGH RISK USB ACTIVITY DETECTED"

    body = f"""
High Risk USB Activity Detected

FILE:
{file_path}

RISK SCORE:
{risk_score}

REASON:
{reason}

Please investigate this activity immediately."""
    
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(
            'smtp.gmail.com', 587
        )

        server.starttls()

        server.login(
            SENDER_EMAIL,
            SENDER_PASSWORD
        )

        server.send_message(msg)
        server.quit()

        print(
            "[+] Email alert sent successfully!"
        )

    except Exception as e:
        print(
            f"[-] Failed to send email alert: {e}"
        )