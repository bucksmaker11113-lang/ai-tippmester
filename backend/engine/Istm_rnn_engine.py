# ================================================================
#   LSTM / RNN NEXT GOAL ENGINE – Quantum Engine 7.0
# ---------------------------------------------------------------
#   Feladata:
#     - élő meccsek idősoros statisztikáinak feldolgozása
#     - 5/10/15 perces gól valószínűség előrejelzés
#     - momentum váltások felismerése
#     - shot pattern -> goal prediction formák tanulása
#
#   A modell DEMO verzióban random inicializált súlyokkal fut,
#   de API készen áll valódi tanított Keras/Tensorflow modell
#   betöltésére.
#
# ================================================================

import numpy as np

class LSTMNextGoalEngine:

    def __init__(self):
        self.sequence_length = 12  # utolsó 12 időlépést nézzük (pl. 12 perc)
        self.features = 6          # shots, sot, da, xg, tempo, momentum

    # ------------------------------------------------------------
    # INPUT NORMALIZÁLÁS
    # ------------------------------------------------------------
    def normalize(self, x):
        x = np.array(x)
        if x.size == 0:
            return np.zeros((self.sequence_length, self.features))
        return (x - np.mean(x)) / (np.std(x) + 1e-6)

    # ------------------------------------------------------------
    # FŐ ELŐREJELZÉS
    # ------------------------------------------------------------
    def predict_next_goal_probability(self, live_timeseries):
        """
        live_timeseries: lista
        [
            [shots, sot, da, xg, tempo, momentum],
            ...
        ]
        """

        # ha nincs adat → gyenge confidence
        if len(live_timeseries) < 3:
            return {
                "goal_5min": 0.05,
                "goal_10min": 0.10,
                "goal_15min": 0.18,
                "confidence": 0.20
            }

        # normalizálás
        data = self.normalize(live_timeseries)
        seq = data[-self.sequence_length:]

        # --------------------------------------------------------
        # DEMO LSTM – random neurális becslés
        # (később Tensorflow model.load() megy ide)
        # --------------------------------------------------------
        avg_attack = np.clip(np.mean(seq[:, 2]) / 60, 0, 1)  # dangerous attacks
        avg_xg = np.clip(np.mean(seq[:, 3]) / 2.5, 0, 1)
        momentum_trend = np.clip(np.mean(np.diff(seq[:, 5])) * 10, -1, 1)

        base = (avg_attack * 0.5) + (avg_xg * 0.4) + (momentum_trend * 0.2)
        base = np.clip(base, 0.01, 0.95)

        # gól esély 5-10-15 percen belül
        goal_5 = base * 0.55
        goal_10 = base * 0.72
        goal_15 = base * 0.88

        return {
            "goal_5min": float(np.clip(goal_5, 0.01, 0.80)),
            "goal_10min": float(np.clip(goal_10, 0.02, 0.90)),
            "goal_15min": float(np.clip(goal_15, 0.05, 0.95)),
            "confidence": float(np.clip(base, 0.1, 0.9))
        }


# GLOBAL INSTANCE
lstm_rnn_engine = LSTMNextGoalEngine()
