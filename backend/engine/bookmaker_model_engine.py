# ==========================================================
#  BOOKMAKER MODEL AI ENGINE – Quantum Engine 7.0
# ==========================================================
#
#   - PinnacleAI      (sharp market)
#   - Bet365AI        (recreational distortion model)
#   - UnibetAI        (mid-sharp)
#   - TippmixProAI    (Hungarian odds-lag predictor)
#
#   Ezekből képződik:
#     * true_fair_odds
#     * bookmaker_resistance
#     * steam_movement_score
#
# ==========================================================

import numpy as np
import torch
import torch.nn as nn


# ----------------------------------------------------------
# 1) Base class – közös viselkedés
# ----------------------------------------------------------

class BookmakerAI(nn.Module):
    def __init__(self, input_dim=3):
        super().__init__()
        self.layers = nn.Sequential(
            nn.Linear(input_dim, 32),
            nn.ReLU(),
            nn.Linear(32, 16),
            nn.ReLU(),
            nn.Linear(16, 1)
        )

    def forward(self, x):
        return self.layers(x)

    def predict(self, prev_odds, cur_odds, volume):
        """Alap odds movement / volume predikció."""
        feats = torch.tensor([
            float(prev_odds),
            float(cur_odds),
            float(volume)
        ], dtype=torch.float32)

        out = self.forward(feats)
        return float(out.item())


# ----------------------------------------------------------
# 2) PINNACLE AI – Sharp Market Predictor
# ----------------------------------------------------------

class PinnacleAI(BookmakerAI):
    """
    A legfontosabb modell.
    A Pinnacle odds → közel a TRUE FAIR ODDS-hoz.
    """

    def predict_fairness(self, prev_odds, cur_odds, sharp_volume):
        sharp_factor = self.predict(prev_odds, cur_odds, sharp_volume)
        fairness = 1 / (cur_odds * (1 - sharp_factor * 0.05))
        return fairness, sharp_factor


# ----------------------------------------------------------
# 3) BET365 AI – Public Bias Predictor
# ----------------------------------------------------------

class Bet365AI(BookmakerAI):
    """
    A Bet365 “public money” torzítás miatt gyakran eltér a fair-től.
    """

    def predict_bias(self, prev_odds, cur_odds, public_money):
        base = self.predict(prev_odds, cur_odds, public_money)
        bias = base * public_money * 0.03
        return bias


# ----------------------------------------------------------
# 4) UNIBET AI – Mid-sharp Blend Model
# ----------------------------------------------------------

class UnibetAI(BookmakerAI):
    """
    Köztes modell: se nem túl sharp, se nem recreational.
    """

    def predict_middle(self, prev_odds, cur_odds, volume):
        mid = self.predict(prev_odds, cur_odds, volume)
        return mid * 0.5


# ----------------------------------------------------------
# 5) TIPPMIXPRO AI – Hungarian Odds Lag Model
# ----------------------------------------------------------

class TippmixProAI(BookmakerAI):
    """
    Magas oddskésés → érték könnyebben található.
    """

    def predict_lag(self, prev_odds, cur_odds, lag_seconds):
        lag_severity = lag_seconds / 60.0
        movement = cur_odds - prev_odds

        # késés miatti torzulás
        lag_effect = movement * lag_severity

        out = self.predict(prev_odds, cur_odds, lag_effect)
        return out, lag_effect


# ----------------------------------------------------------
# 6) MULTI-BOOKMAKER INTEGRÁCIÓ
# ----------------------------------------------------------

class BookmakerModelEngine:
    def __init__(self):
        self.pinnacle = PinnacleAI()
        self.bet365 = Bet365AI()
        self.unibet = UnibetAI()
        self.tpro = TippmixProAI()

    def compute_true_fair(self, data):
        """
        A világ legvalószínűbb FAIR ODDS értéke:
        több bookmaker AI eredményének súlyozott összege.
        """

        pinnacle_fair, sharp_factor = self.pinnacle.predict_fairness(
            data["pin_prev"], data["pin_cur"], data["pin_volume"]
        )

        bet365_bias = self.bet365.predict_bias(
            data["b365_prev"], data["b365_cur"], data["public_money"]
        )

        unibet_mid = self.unibet.predict_middle(
            data["uni_prev"], data["uni_cur"], data["uni_volume"]
        )

        tlag, lag_effect = self.tpro.predict_lag(
            data["tpro_prev"], data["tpro_cur"], data["tpro_lag"]
        )

        # Súlyozott FAIR ODDS:
        true_fair = (
            (1 / pinnacle_fair) * 0.55 +   # sharp line
            (1 / (data["b365_cur"] + bet365_bias)) * 0.2 +
            (1 / (data["uni_cur"] + unibet_mid)) * 0.15 +
            (1 / (data["tpro_cur"] + lag_effect)) * 0.10
        )

        true_fair = 1 / max(true_fair, 0.001)

        return {
            "true_fair_odds": true_fair,
            "sharp_factor": sharp_factor,
            "bet365_bias": bet365_bias,
            "unibet_mid": unibet_mid,
            "tpro_lag_effect": lag_effect
        }

    def compute_bookmaker_resistance(self, movement, volatility, sharp_factor):
        """
        Mennyire “ellenálló” a piac → minél nagyobb, annál nehezebb value-t találni.
        """
        bri = (
            abs(movement) * 0.4 +
            volatility * 0.3 +
            (1 - sharp_factor) * 0.3
        )
        return float(bri)

    def compute_steam_score(self, prev, cur, sharp_volume):
        """
        Steam = hirtelen, erős piaci elmozdulás.
        """
        move = prev - cur
        steam = move * sharp_volume
        return float(steam)


# ----------------------------------------------------------
# GLOBAL INSTANCE
# ----------------------------------------------------------

bookmaker_engine = BookmakerModelEngine()
