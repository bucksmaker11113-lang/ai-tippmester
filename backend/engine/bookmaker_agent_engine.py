# ==============================================================================
#   BOOKMAKER AGENT ENGINE – Tippmester Quantum Engine 7.0
# ------------------------------------------------------------------------------
#   Feladata:
#     - odds mozgás elemzése
#     - sharp money felismerése
#     - public money ellenhatás
#     - steam move / manipulation detektálás
#
#   Kimenet:
#     "market_pressure": 0–1
#     "steam_risk": 0–1
#     "sharp_conf": 0–1
#     "agent_score": 0–1
# ==============================================================================

import numpy as np

class BookmakerAgentEngine:

    def __init__(self):
        pass

    # -----------------------------------------------------------
    # Sharp money = gyors odds esés kicsi piacon
    # -----------------------------------------------------------
    def detect_sharp(self, odds_history):
        if len(odds_history) < 3:
            return 0.2

        diffs = np.diff(odds_history)
        sharp = float(np.clip(np.abs(np.min(diffs)) * 5, 0, 1))
        return sharp

    # -----------------------------------------------------------
    # Steam = nagy tömeg pénz → odds beszakad
    # -----------------------------------------------------------
    def detect_steam(self, odds_history):
        if len(odds_history) < 4:
            return 0.1

        volatility = np.std(odds_history[-5:])
        steam = float(np.clip(volatility * 3, 0, 1))
        return steam

    # -----------------------------------------------------------
    # Market pressure = mennyire aktív a piac
    # -----------------------------------------------------------
    def market_pressure(self, volume, volatility):
        base = (volume * 0.6 + volatility * 0.4) / 100
        return float(np.clip(base, 0.05, 1.0))

    # -----------------------------------------------------------
    # Fő agent predikció
    # -----------------------------------------------------------
    def analyze_market(self, odds_history, volume, volatility):
        sharp_conf = self.detect_sharp(odds_history)
        steam_risk = self.detect_steam(odds_history)
        mkt_press = self.market_pressure(volume, volatility)

        agent_score = float(np.clip(
            sharp_conf * 0.5 + mkt_press * 0.3 - steam_risk * 0.2,
            0.05, 1.0
        ))

        return {
            "sharp_conf": sharp_conf,
            "steam_risk": steam_risk,
            "market_pressure": mkt_press,
            "agent_score": agent_score
        }


# GLOBAL INSTANCE
bookmaker_agent = BookmakerAgentEngine()
