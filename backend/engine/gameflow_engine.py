# ============================================================================
#   Gameflow Engine – Tippmester Quantum Engine
#   Élő meccs események elemzése (tempo, momentum, shot intensity, attack rate)
# ============================================================================

import numpy as np
import random
import math


class GameflowEngine:

    def __init__(self):
        # alap meccs tempó
        self.base_tempo = 0.5
        self.base_pressure = 0.5
        self.base_momentum = 0.5

    # ----------------------------------------------------------------------
    # Tempó becslése (lövések, támadások, sebesség)
    # ----------------------------------------------------------------------
    def estimate_tempo(self, event):
        """
        event expected:
            - shots_last_10
            - attacks_last_10
            - dangerous_attacks_last_10
        """

        shots = event.get("shots_last_10", 4)
        attacks = event.get("attacks_last_10", 8)
        danger = event.get("dangerous_attacks_last_10", 3)

        raw = shots * 0.4 + attacks * 0.3 + danger * 0.6

        tempo = raw / 25
        return max(0.05, min(1.0, tempo))

    # ----------------------------------------------------------------------
    # Pressing intensity
    # ----------------------------------------------------------------------
    def estimate_pressure(self, event):
        pressure = (
            event.get("pressing_actions", 10) * 0.1 +
            event.get("high_regains", 2) * 0.2
        ) / 10

        return max(0.05, min(1.0, pressure))

    # ----------------------------------------------------------------------
    # Momentum
    # ----------------------------------------------------------------------
    def estimate_momentum(self, event):
        # egyszerű momentum modell:
        # ha az egyik csapat több veszélyes támadást gyárt → momentum
        m = (
            event.get("danger_home", 5) -
            event.get("danger_away", 5)
        )

        # 0–1 skálán
        mom = 0.5 + (m * 0.03)
        return max(0.01, min(0.99, mom))

    # ----------------------------------------------------------------------
    # Publikus API – "live prediction index"
    # ----------------------------------------------------------------------
    def predict(self, event):
        tempo = self.estimate_tempo(event)
        pressure = self.estimate_pressure(event)
        momentum = self.estimate_momentum(event)

        # összesített attacking threat index
        score = (
            tempo * 0.45 +
            pressure * 0.30 +
            momentum * 0.25
        )

        return max(0.01, min(0.99, score))
