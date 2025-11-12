"""
Value Analyzer
Odds és statisztikai alapú value-score számítás.
"""

import math
import random

class ValueAnalyzer:
    def __init__(self):
        pass

    def evaluate_odds(self, odds, stats):
        """Visszaad egy 0–1 közötti value értéket"""
        if not odds:
            return 0.5
        try:
            avg_odds = sum(odds.values()) / len(odds)
            score = 1 / avg_odds + random.uniform(-0.05, 0.05)
            return round(max(min(score, 1.0), 0.0), 2)
        except Exception:
            return 0.5
