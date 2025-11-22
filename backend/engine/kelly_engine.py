# ============================================================================
#   Kelly Engine – Tippmester Quantum Engine
#   Bankroll optimalizáló modul (Kelly-criterion, risk adjust)
# ============================================================================

import math


class KellyEngine:

    def __init__(self):
        # sportág súlyok
        self.sport_weights = {
            "football": 1.00,
            "basketball": 0.85,
            "hockey": 0.90,
            "tennis": 0.75
        }

        # bankroll százalék limitek
        self.max_stake_single = 0.02    # max 2%
        self.max_stake_kombi = 0.01     # max 1%
        self.max_stake_live = 0.015     # max 1.5%

    # ----------------------------------------------------------------------
    # Sportág meghatározása
    # ----------------------------------------------------------------------
    def get_sport(self, event):
        s = event.get("sport", "football").lower()
        return self.sport_weights.get(s, 1.0)

    # ----------------------------------------------------------------------
    # Kelly formula
    # ----------------------------------------------------------------------
    def kelly_fraction(self, value, fair_odds):
        """ value = adjusted_fair_odds - market_odds """
        if fair_odds <= 1:
            return 0

        b = fair_odds - 1  # net odds
        p = 1 / fair_odds  # implied probability
        q = 1 - p

        try:
            f = (b * p - q) / b
        except ZeroDivisionError:
            return 0

        return max(0, f)

    # ----------------------------------------------------------------------
    # Publikus API – stake számítás
    # ----------------------------------------------------------------------
    def calculate(self, value, fair_odds, event=None):
        sport_weight = 1.0
        if event:
            sport_weight = self.get_sport(event)

        base_fraction = self.kelly_fraction(value, fair_odds)

        # sport súlyozás
        weighted = base_fraction * sport_weight

        # tét-típus alapján limitálás
        tip_type = event.get("tip_type", "single")

        if tip_type == "single":
            weighted = min(weighted, self.max_stake_single)

        elif tip_type == "kombi":
            weighted = min(weighted, self.max_stake_kombi)

        elif tip_type == "live":
            weighted = min(weighted, self.max_stake_live)

        # minimum 0.1% ha value > 0
        if weighted > 0:
            weighted = max(weighted, 0.001)

        return round(weighted, 5)
