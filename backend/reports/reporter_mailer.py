"""
Report Mailer – Tippmester 5.2
Napi e-mail küldés Gmail SMTP-n keresztül.
"""

import smtplib
from email.mime.text import MIMEText

class ReportMailer:
    def __init__(self, email, password):
        self.email = email
        self.password = password

    def send_email(self, subject, body, to=None):
        to = to or self.email
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = self.email
        msg["To"] = to

        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(self.email, self.password)
                server.send_message(msg)
            print("✅ Riport e-mail sikeresen elküldve.")
        except Exception as e:
            print(f"⚠️ E-mail küldési hiba: {e}")
