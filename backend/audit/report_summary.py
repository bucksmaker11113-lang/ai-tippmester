"""
Report Summary – Tippmester AI Fusion 1.0
Napi teljesítmény összesítő riport generálása.
"""

import pandas as pd

class ReportSummary:
    def __init__(self, performance_log="backend/data/performance_log.json"):
        self.path = performance_log

    def generate_summary(self):
        try:
            df = pd.read_json(self.path)
            win_rate = (df["result"] == "win").sum() / len(df)
            avg_conf = df["confidence"].mean()
            return {
                "total_tips": len(df),
                "win_rate": round(win_rate * 100, 2),
                "avg_confidence": round(avg_conf, 2)
            }
        except Exception:
            return {"total_tips": 0, "win_rate": 0, "avg_confidence": 0}

