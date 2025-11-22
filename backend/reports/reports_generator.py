"""
Report Generator – Tippmester AI Fusion 1.0
Napi jelentések és statisztikai összefoglalók generálása.
"""

import csv
from datetime import datetime
from backend.audit.report_summary import ReportSummary

class ReportGenerator:
    def __init__(self):
        self.summary = ReportSummary()

    def generate_daily_report(self, output_file="backend/reports/daily_report.csv"):
        data = self.summary.generate_summary()
        data["date"] = datetime.now().strftime("%Y-%m-%d")
        with open(output_file, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=data.keys())
            if f.tell() == 0:
                writer.writeheader()
            writer.writerow(data)
        return data

