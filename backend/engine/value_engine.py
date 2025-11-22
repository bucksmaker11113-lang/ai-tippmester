# ============================================================================
#   Value Engine – Tippmester Quantum Engine
#   Expected value, fair odds, bias correction, bookmaker margin
# ============================================================================

import math


class ValueEngine:

    def __init__(self):
        self.margin_baseline = 0.07  # átlagos bookmaker margin

    # ----------------------------------------------------------------------
    # Fair odds kalkuláció
    # ----------------------------------------------------------------------
    def compute_fair_odds(self, probability):
        if probability <= 0:
            return 99.99
        return 1 / probability

    # ----------------------------------------------------------------------
    # Bookmaker margin becslése
    # ----------------------------------------------------------------------
    def estimate_margin(self, event):
        odds = event.get("odds", 2.0)
        open_odds = event.get("odds_open", odds)

        implied_now = 1 / odds
        implied_open = 1 / open_odds

        drift = abs(implied_now - implied_open)

        margin = self.margin_baseline + drift * 0.4
        return min(0.20, max(0.01, margin))

    # ----------------------------------------------------------------------
    # Expected Value számítás
    # ----------------------------------------------------------------------
    def calculate(self, event, fair_odds):
        market_odds = event.get("odds", 2.0)

        margin = self.estimate_margin(event)
        adjusted_fair_odds = fair_odds * (1 + margin)

        # EV = fair - market
        value = adjusted_fair_odds - market_odds

        return value
