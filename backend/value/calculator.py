"""
Value Calculator – Tippmester AI Fusion 1.0
Matematikai értékelés odds + stat alapján.
"""

import math
import random

class ValueCalculator:
    def calculate(self, odds, probability):
        """Egyszerű value képlet: (odds * prob) - 1"""
        return round((odds * probability) - 1, 3)

    def expected_value(self, picks):
        """Több tipp átlagos várható értéke."""
        if not picks:
            return 0.0
        return round(sum(p["value_score"] for p in picks) / len(picks), 3)

