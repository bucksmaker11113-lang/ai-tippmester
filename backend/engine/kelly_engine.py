# =====================================================================
#   KELLY CRITERION ENGINE – Tippmester Quantum Engine 7.0
# ---------------------------------------------------------------------
# Feladata:
#   - bankroll optimális növelése
#   - tét meghatározása value tippek alapján
#   - single / kombi / live külön bankroll logika
#   - túlzott kockázat elleni védelem (fractional Kelly)
#
# =====================================================================

import numpy as np

class KellyEngine:

    def __init__(self, kelly_fraction=0.25):
        """
        kelly_fraction:
            1.0  = full Kelly (agresszívabb)
            0.25 = quarter Kelly (biztonságosabb – ez ajánlott fogadásnál)
        """
        self.kelly_fraction = kelly_fraction

    # ----------------------------------------------------------------
    # Kelly formula:
    #   f* = (b*p - q) / b
    # ----------------------------------------------------------------
    def kelly_fraction_calc(self, odds, win_prob):
        """
        odds: valós odds
        win_prob: modell által becsült valószínűség (0–1)
        """
        b = odds - 1
        p = win_prob
        q = 1 - p

        k = (b * p - q) / b
        return float(np.clip(k, 0.0, 1.0))

    # ----------------------------------------------------------------
    # Tét meghatározása adott bankrollhoz
    # ----------------------------------------------------------------
    def stake(self, bankroll, odds, win_prob):
        k = self.kelly_fraction_calc(odds, win_prob)
        stake_raw = bankroll * k * self.kelly_fraction

        # túl magas tét ellen védelem
        stake_final = float(np.clip(stake_raw, 0, bankroll * 0.05))  # max 5%

        return round(stake_final, 2)

    # ----------------------------------------------------------------
    # Single / Kombi / Live bankroll külön kezelése
    # ----------------------------------------------------------------
    def allocate(self, bankrolls, tip_type, odds, win_prob):
        """
        bankrolls: dict:
            {
                "single": 300000,
                "kombi": 300000,
                "live": 300000
            }
        tip_type: "single" / "kombi" / "live"
        """

        br = float(bankrolls.get(tip_type, 0))
        if br <= 0:
            return 0

        return self.stake(br, odds, win_prob)


# GLOBAL INSTANCE
kelly_engine = KellyEngine(kelly_fraction=0.25)
