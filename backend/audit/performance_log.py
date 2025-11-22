"""
Performance Log – Tippmester AI Fusion 1.0
AI tippek teljesítményének rögzítése.
"""

import json
from datetime import datetime

class PerformanceLog:
    def __init__(self, filepath="backend/data/performance_log.json"):
        self.path = filepath
        self.entries = []

    def record(self, match, result, confidence):
        self.entries.append({
            "match": match,
            "result": result,
            "confidence": confidence,
            "timestamp": datetime.now().isoformat()
        })
        self._save()

    def _save(self):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.entries, f, indent=2, ensure_ascii=False)

