"""
Self Audit – Tippmester AI Fusion 1.0
Napi AI teljesítmény önellenőrzés.
"""

import csv
from datetime import datetime

class SelfAudit:
    def __init__(self, filepath="backend/data/self_audit_log.csv"):
        self.path = filepath
        self.entries = []

    def log(self, category, value):
        self.entries.append({"category": category, "value": value, "time": datetime.now().isoformat()})
        self._save()

    def _save(self):
        with open(self.path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=self.entries[0].keys())
            writer.writeheader()
            writer.writerows(self.entries)

