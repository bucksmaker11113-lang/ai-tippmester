# ============================================================================
#   Bookmaker Engine – Tippmester Quantum Engine
#   Bookmaker manipuláció / odds pressure / sharp money detektor
# ============================================================================

import numpy as np
import random
import math


class BookmakerEngine:

    def __init__(self):
        # baseline manipulatív odds-eltérés
        self.pressure_baseline = 0.5

    # ----------------------------------------------------------------------
    # Odds pressure felmérés
    # ----------------------------------------------------------------------
    def calculate_pressure(self, event):
        """
        event fields:
            odds_open
            odds_current
            volume
            bookmaker_rank
        """

        open_o = event.get("odds_open", 2.0)
        current_o = event.get("odds_current", open_o)
        volume = event.get("volume", 0.5)
        bk_rank = event.get("bookmaker_rank", 0.5)

        # odds mozgás
        diff = abs(open_o - current_o)

        # sharp money (ha a volume nagy, odds mégis esik/femelkedik)
        sharp_factor = volume * (diff * 2)

        # bookmaker rank (1 = profi, 0 = amatőr)
        rank_factor = (1.2 - bk_rank)

        pressure = diff * 0.5 + sharp_factor * 0.3 + rank_factor * 0.2

        return min(1.0, max(0.0, pressure))

    # ----------------------------------------------------------------------
    # Publikus API – manipulációs érték visszaadása
    # ----------------------------------------------------------------------
    def detect(self, event):
        pressure = self.calculate_pressure(event)

        # adaptáció: baseline finomítása
        self.pressure_baseline = (
            self.pressure_baseline * 0.8 + pressure * 0.2
        )

        # visszaadott érték: 0.01–0.99 piaci manipuláció index
        return max(0.01, min(0.99, self.pressure_baseline))
