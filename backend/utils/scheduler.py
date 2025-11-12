"""
Scheduler – Tippmester 5.2
Időzített riport és tanulási futások.
"""

import schedule
import time
from backend.reports.auto_reporter import AutoReporter

class Scheduler:
    def __init__(self, email, password):
        self.auto_reporter = AutoReporter(email, password)

    def start(self):
        schedule.every().day.at("22:30").do(self.auto_reporter.run_daily)
        print("🕒 Napi riport időzítve 22:30-ra.")
        while True:
            schedule.run_pending()
            time.sleep(60)
