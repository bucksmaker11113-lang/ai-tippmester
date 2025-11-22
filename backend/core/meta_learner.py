"""
Meta Learner - Tippmester AI Fusion 1.0
Öntanuló modul: figyeli a múltbeli teljesítményt, és súlyozza az új tippeket.
"""

import json
from datetime import datetime

class MetaLearner:
    def __init__(self):
        self.performance_log = []
        self.bias_memory = {}

    def calculate_confidence(self, base_value, correction):
        weight = 0.7 * base_value + 0.3 * (1 - abs(correction))
        return round(min(max(weight, 0.1), 0.99), 2)

    def update_performance(self, match, correct):
        entry = {"match": match, "correct": correct, "date": datetime.now().isoformat()}
        self.performance_log.append(entry)

    def export_log(self, filepath="backend/data/meta_log.json"):
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(self.performance_log, f, indent=2, ensure_ascii=False)

