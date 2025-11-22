"""
Live Odds Monitor – Tippmester AI Fusion 1.0
Valós idejű odds esés figyelő modul.
"""

import random
import time

class LiveOddsMonitor:
    def __init__(self):
        self.previous_odds = {}

    def update(self, match, current_odds):
        """Észleli a gyors odds változásokat."""
        old = self.previous_odds.get(match, current_odds)
        alerts = {}
        for key in current_odds:
            diff = current_odds[key] - old.get(key, current_odds[key])
            if abs(diff) >= 0.3:
                alerts[key] = diff
        self.previous_odds[match] = current_odds
        return alerts

