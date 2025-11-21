# ====================================================================
#                  GAMEFLOW ENGINE – Tippmester Quantum Engine 7.0
# --------------------------------------------------------------------
# Feladata:
#   - élő meccs statisztikák alapján momentum & tempó becslés
#   - veszélyzóna analízis
#   - xG trend előrejelzés
#   - shot pattern → goal flow előrejelzés
#   - integráció: LSTM/RNN Next Goal Engine
#
# Bemenet:
#   live_stats: dict  (utolsó 5–20 perc)
#   például:
#        {
#           "shots": [...],
#           "shots_on_target": [...],
#           "dangerous_attacks": [...],
#           "xg": [...],
#           "possession": [...],
#           "tempo": [...],
#           "momentum": [...]
#        }
#
# Kimenet:
#   {
#       "xg_trend": float,
#       "momentum": float,
#       "tempo": float,
#       "danger_zone": float,
#       "lstm": {...},
#       "goal_chance": float,
#       "confidence": float
#   }
#
# ====================================================================

import numpy as np
from engine.lstm_rnn_engine import lstm_rnn_engine


class GameFlowEngine:

    def __init__(self):
        self.min_samples = 4

    # -----------------------------------------------------------
    # Biztonságos list → float konverzió
    # -----------------------------------------------------------
    def safe_avg(self, arr):
        if not arr or len(arr) == 0:
            return 0.0
        return float(np.mean(arr))

    # -----------------------------------------------------------
    # xG trend becslése (lineáris regresszió szerű)
    # -----------------------------------------------------------
    def estimate_xg_trend(self, xg_list):
        if len(xg_list) < 2:
            return 0.0
        diffs = np.diff(xg_list[-5:])
        trend = np.clip(np.mean(diffs), -0.5, 1.0)
        return float(trend)

    # -----------------------------------------------------------
    # momentum becslés
    # -----------------------------------------------------------
    def estimate_momentum(self, attacks, shots, sot):
        att = self.safe_avg(attacks)
        st = self.safe_avg(shots)
        sotv = self.safe_avg(sot)

        momentum = (att * 0.5 + st * 0.3 + sotv * 0.2) / 100
        return float(np.clip(momentum, 0, 1))

    # -----------------------------------------------------------
    # veszélyzóna érték
    # -----------------------------------------------------------
    def estimate_danger_zone(self, da_list, xg_list):
        da = self.safe_avg(da_list)
        xg = self.safe_avg(xg_list)
        danger = (da / 50) * 0.6 + (xg / 2.5) * 0.4
        return float(np.clip(danger, 0, 1))

    # -----------------------------------------------------------
    # fő metódus: NEXT GAMEFLOW PREDICTION
    # -----------------------------------------------------------
    def predict_next_gameflow(self, live_stats):
        """
        Élő meccs statisztikák → gameflow + LSTM predikció
        """

        # Ha nincs adat → default érték
        if "shots" not in live_stats or len(live_stats["shots"]) < self.min_samples:
            return {
                "xg_trend": 0.0,
                "momentum": 0.1,
                "tempo": 0.1,
                "danger_zone": 0.1,
                "lstm": {},
                "goal_chance": 0.05,
                "confidence": 0.2
            }

        # Alap statisztikák
        shots = live_stats.get("shots", [])
        sot = live_stats.get("shots_on_target", [])
        da = live_stats.get("dangerous_attacks", [])
        xg = live_stats.get("xg", [])
        tempo_list = live_stats.get("tempo", [])
        momentum_list = live_stats.get("momentum", [])

        # ------------------------------
        # FŐ LÉPÉS: alap gameflow elemzés
        # ------------------------------

        xg_trend = self.estimate_xg_trend(xg)
        momentum_est = self.estimate_momentum(da, shots, sot)
        danger_zone = self.estimate_danger_zone(da, xg)
        tempo = self.safe_avg(tempo_list)

        # ------------------------------
        # LSTM/RNN NEXT GOAL PREDICTION
        # ------------------------------

        # Idősoros inputok megépítése az LSTM motor számára
        sequence = []
        for i in range(len(shots)):
            sequence.append([
                shots[i],
                sot[i] if i < len(sot) else 0,
                da[i] if i < len(da) else 0,
                xg[i] if i < len(xg) else 0,
                tempo_list[i] if i < len(tempo_list) else 0,
                momentum_list[i] if i < len(momentum_list) else 0,
            ])

        lstm_pred = lstm_rnn_engine.predict_next_goal_probability(sequence)

        # ------------------------------
        # Integrációs értékek
        # ------------------------------

        # goal chance = 10 perc gól esély
        goal_chance = lstm_pred["goal_10min"]

        # combined confidence
        confidence = float(np.clip(
            (momentum_est * 0.4) +
            (danger_zone * 0.3) +
            (xg_trend * 0.2) +
            (lstm_pred["confidence"] * 0.7),
            0.05,
            1.0
        ))

        return {
            "xg_trend": float(xg_trend),
            "momentum": float(momentum_est),
            "tempo": float(tempo),
            "danger_zone": float(danger_zone),
            "lstm": lstm_pred,
            "goal_chance": float(goal_chance),
            "confidence": float(confidence)
        }


# GLOBAL INSTANCE
gameflow_engine = GameFlowEngine()
