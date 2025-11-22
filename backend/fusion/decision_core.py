"""
Decision Core – Tippmester AI Fusion 1.0
Sportág-prioritás és döntési súlyozás.
"""

import random

class DecisionCore:
    def __init__(self):
        self.weights = {"foci": 0.5, "tenisz": 0.2, "kosár": 0.2, "hoki": 0.1}

    def update_weights(self, performance_stats):
        for sport, roi in performance_stats.items():
            if sport in self.weights:
                self.weights[sport] = max(0.05, min(0.7, self.weights[sport] + (roi / 100)))
        return self.weights

    def get_top_sport(self):
        return max(self.weights, key=self.weights.get)

