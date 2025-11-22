"""
Smart Hedge Manager – Tippmester AI Fusion 1.0
Valós idejű fedező tipp javaslat odds mozgások alapján.
"""

import random

class HedgeManager:
    def __init__(self):
        self.hedge_log = []

    def suggest_hedge(self, current_odds, previous_odds):
        """Észleli a nagy odds mozgást és fedező irányt javasol."""
        for outcome in current_odds:
            diff = current_odds[outcome] - previous_odds.get(outcome, current_odds[outcome])
            if abs(diff) > 0.25:
                hedge = "X" if outcome != "X" else "1"
                self.hedge_log.append((outcome, hedge, diff))
                return {"hedge_tip": hedge, "odds_change": diff}
        return None

