"""
Value Tracker – Tippmester AI Fusion 1.0
Value anomáliák naplózása és napi összegzés.
"""

import csv
from datetime import datetime

class ValueTracker:
    def __init__(self, filepath="backend/data/value_history.db"):
        self.filepath = filepath
        self.values = []

    def log_value(self, match, value_score, odds):
        entry = {
            "match": match,
            "value_score": value_score,
            "avg_odds": sum(odds.values()) / len(odds),
            "timestamp": datetime.now().isoformat()
        }
        self.values.append(entry)
        self._save()

    def _save(self):
        with open(self.filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=self.values[0].keys())
            writer.writeheader()
            writer.writerows(self.values)

