# ============================================================================
#   Poisson Engine – Tippmester Quantum Engine
#   Várható gólok, score distribution és támadási intenzitás becslése.
#   Könnyített Poisson-modell.
# ============================================================================

import numpy as np
import math
import random


class PoissonEngine:

    def __init__(self):
        pass

    # ----------------------------------------------------------------------
    # Várható gól kiszámítása
    # ----------------------------------------------------------------------
    def expected_goals(self, event):
        attack = event.get("attack_strength", 1.0)
        defense = event.get("defense_weakness", 1.0)
        tempo = event.get("tempo", 1.0)

        # egyszerű xG modell
        xg = (attack * tempo) / max(0.3, defense)

        return max(0.1, min(3.5, xg))

    # ----------------------------------------------------------------------
    # Poisson formula
    # ----------------------------------------------------------------------
    def poisson_pmf(self, lam, k):
        try:
            return (lam ** k * math.exp(-lam)) / math.factorial(k)
        except OverflowError:
            return 0.0

    # ----------------------------------------------------------------------
    # Score distribution build
    # ----------------------------------------------------------------------
    def score_distribution(self, event):
        lam = self.expected_goals(event)

        dist = {}
        for k in range(0, 6):   # 0–5 gólig
            dist[k] = self.poisson_pmf(lam, k)

        return dist

    # ----------------------------------------------------------------------
    # Publikus API
    # ----------------------------------------------------------------------
    def predict(self, event):
        dist = self.score_distribution(event)

        # gól várható értéke 0–1 skálán
        expected_goal_index = dist.get(1, 0) + dist.get(2, 0) * 1.5 + dist.get(3, 0) * 2

        return max(0.01, min(0.99, expected_goal_index))
