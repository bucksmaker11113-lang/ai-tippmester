"""
Auto Reporter – Tippmester AI Fusion 1.0
Automatikus napi riport generálás és e-mail küldés.
"""

from datetime import datetime
from backend.reports.report_generator import ReportGenerator
from backend.reports.report_mailer import ReportMailer

class AutoReporter:
    def __init__(self, email, password):
        self.generator = ReportGenerator()
        self.mailer = ReportMailer(email, password)

    def run_daily(self):
        report = self.generator.generate_daily_report()
        subject = f"Tippmester napi riport – {datetime.now().strftime('%Y.%m.%d')}"
        body = f"""Szia!

Ez a Tippmester AI 5.2 automatikus napi riportja:

📊 Tippek száma: {report['total_tips']}
✅ Találati arány: {report['win_rate']}%
🧠 Átlagos bizalom: {report['avg_confidence']}

Üdv,
Mesterke 🤖"""
        self.mailer.send_email(subject, body)
        return report

