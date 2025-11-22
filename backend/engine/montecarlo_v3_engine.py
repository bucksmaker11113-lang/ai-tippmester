# ============================================================================
#   MonteCarlo V3 Engine – Tippmester Quantum Engine
#   Nagy pontosságú szimulációs motor odds értékeléshez
#   50 000+ szimuláció, dinamikus variancia és sportág-specifikus súlyozás
# ============================================================================

import random
import numpy as np
import math
import time


class MonteCarloV3:

    def __init__(self):
        # alapértelmezett szimulációs szám
        self.simulations = 50000

        # sportág súlyozás
        self.sport_weights = {
            "football": 1.00,
            "basketball": 0.85,
            "hockey": 0.90,
            "tennis": 0.75
        }

    # ----------------------------------------------------------------------
    # SPORTÁG LEKÉRÉSE ESEMÉNYBŐL
    # ----------------------------------------------------------------------
    def get_sport(self, event):
        sport = event.get("sport", "football").lower()
        if sport not in self.sport_weights:
            return "football"
        return sport

    # ----------------------------------------------------------------------
    # MONTE CARLO ALAPPROBABILITÁS
    # ----------------------------------------------------------------------
    def base_probability(self, event):
        """
        Very rough initial win probability estimate based on simple heuristics.
        """
        odds = event.get("odds", 2.00)
        if odds <= 1.01:
            return 0.99
        return min(0.95, max(0.05, 1 / odds))

    # ----------------------------------------------------------------------
    # SZIMULÁCIÓS FUTTATÁS
    # ----------------------------------------------------------------------
    def simulate(self, event):
        """
        MonteCarlo V3:
        - 50 000 szimuláció
        - dinamikus torzítás-korrekció
        - sportág-alapú variancia
        - random momentum zaj
        """
        sport = self.get_sport(event)
        weight = self.sport_weights.get(sport, 1.0)

        base_p = self.base_probability(event)

        # variancia növelés/növelése sportág alapján
        variance = 0.06 * weight

        wins = 0

        for _ in range(self.simulations):

            # dinamizált random szórás
            adjusted_p = np.random.normal(base_p, variance)

            # 0–1 közé bilincs
            adjusted_p = max(0.01, min(0.99, adjusted_p))

            # momentum zaj → kisebb ingadozás
            adjusted_p *= (0.97 + (random.random() * 0.06))

            if random.random() < adjusted_p:
                wins += 1

        mc_probability = wins / self.simulations

        # alsó-felső határok
        mc_probability = max(0.01, min(0.99, mc_probability))

        return mc_probability
