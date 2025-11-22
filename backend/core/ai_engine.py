"""
Tippmester AI Fusion 1.0 - AI Engine
Fő döntésmotor: odds, statisztika és tanulási rétegek kombinációja.
"""

import random
import math
from datetime import datetime
from .meta_learner import MetaLearner
from .bias_engine import BiasCorrector
from .value_analyzer import ValueAnalyzer

class TippmesterAI:
    def __init__(self):
        self.meta = MetaLearner()
        self.bias = BiasCorrector()
        self.value = ValueAnalyzer()
        self.history = []

    def analyze_match(self, match_data):
        """Elemzi a meccset és visszaad egy tippajánlatot."""
        odds = match_data.get("odds", {})
        stats = match_data.get("stats", {})
        team_a, team_b = match_data.get("teams", ("", ""))

        base_value = self.value.evaluate_odds(odds, stats)
        correction = self.bias.adjust_for_bias(team_a, team_b)
        confidence = self.meta.calculate_confidence(base_value, correction)

        # végső döntés logikája
        pick = self._choose_outcome(odds, confidence)
        timestamp = datetime.now().isoformat()

        result = {
            "match": f"{team_a} vs {team_b}",
            "pick": pick,
            "confidence": confidence,
            "odds": odds.get(pick),
            "timestamp": timestamp
        }
        self.history.append(result)
        return result

    def _choose_outcome(self, odds, confidence):
        """Döntés: 1, X vagy 2"""
        options = ["1", "X", "2"]
        weighted = [confidence * random.random() for _ in options]
        return options[weighted.index(max(weighted))]

    def get_history(self):
        return self.history

