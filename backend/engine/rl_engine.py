# ============================================================================
#   RL Engine – Reinforcement Learning alapú piaci adaptáció
#   Tippmester Quantum Engine
#   A modul tanul az odds változásából és piaci hatásokból.
# ============================================================================

import random
import numpy as np


class RLEngine:

    def __init__(self):
        # tanulási paraméterek
        self.alpha = 0.35     # learning rate
        self.gamma = 0.85     # discount factor

        # piaci stabilitási baseline
        self.market_stability = 0.5

    # ----------------------------------------------------------------------
    # Piaci reakció becslése
    # ----------------------------------------------------------------------
    def estimate_market_reaction(self, event):
        """
        input:
            event = {
                "odds_open": float,
                "odds_current": float,
                "volume": float (fogadási aktivitás),
                ...
            }
        """

        o_open = event.get("odds_open", 2.00)
        o_now = event.get("odds_current", o_open)
        volume = event.get("volume", 0.5)

        # odds változás mértéke
        shift = abs(o_open - o_now)

        # normalizált piaci zaj
        noise = min(1.0, shift * 0.8 + volume * 0.2)

        return noise

    # ----------------------------------------------------------------------
    # RL frissítés – piaci tanulás
    # ----------------------------------------------------------------------
    def adapt(self, event):
        """
        RL value update:
            new_state = old + alpha * (reward + gamma * next - old)
        """

        market_noise = self.estimate_market_reaction(event)

        # jutalmazás: erős piaci mozgás → korrigálni kell a valószínűséget
        reward = (1 - market_noise)

        # RL update
        self.market_stability = (
            self.market_stability +
            self.alpha * (reward + self.gamma * market_noise - self.market_stability)
        )

        # skála: 0.01 – 0.99
        return max(0.01, min(0.99, self.market_stability))
