"""
File Manager – Tippmester 5.2
Adat- és riportfájlok karbantartása.
"""

import os

class FileManager:
    def __init__(self, base_path="backend/data/"):
        self.base_path = base_path

    def ensure_files(self):
        os.makedirs(self.base_path, exist_ok=True)
        defaults = [
            "bankroll_profiles.csv",
            "value_history.db",
            "conversation_history.db",
            "self_audit_log.csv",
            "performance_log.json"
        ]
        for f in defaults:
            path = os.path.join(self.base_path, f)
            if not os.path.exists(path):
                open(path, "w").close()
