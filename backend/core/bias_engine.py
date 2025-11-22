"""
Predictive Bias Engine
Torzítások felismerése és korrekciója.
"""

import random

class BiasCorrector:
    def __init__(self):
        self.bias_map = {}

    def adjust_for_bias(self, team_a, team_b):
        key = f"{team_a}_{team_b}"
        bias = self.bias_map.get(key, random.uniform(-0.1, 0.1))
        self.bias_map[key] = bias
        return bias

    def update_bias(self, team, outcome):
        """Ha egy csapatnál sorozatosan téved az AI, finoman korrigál."""
        old_bias = self.bias_map.get(team, 0.0)
        new_bias = old_bias + (0.05 if outcome == "loss" else -0.03)
        self.bias_map[team] = max(min(new_bias, 0.5), -0.5)
