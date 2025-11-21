# ==========================================================
#   MULTI-AGENT AI ENGINE – Tippmester Quantum Engine 7.0
# ==========================================================
#
#   5 külön AI ügynök:
#     1) ValueFinder
#     2) MomentumHunter
#     3) MarketReader
#     4) RiskMaster
#     5) QuantumSynth (meta-AI)
#
#   Minden AI egy-egy specialista.
#   A QuantumSynth végül súlyozott döntést hoz.
#
# ==========================================================

import numpy as np
import torch
import torch.nn as nn

from database.db import SessionLocal
from database.models import OddsHistory, LiveStatsHistory, TipSingle, TipLive


# ----------------------------------------------------------
# 1) ValueFinder AI — Odds & Value specialist
# ----------------------------------------------------------

class ValueFinderAI(nn.Module):
    def __init__(self):
        super().__init__()
        self.layers = nn.Sequential(
            nn.Linear(4, 16),
            nn.ReLU(),
            nn.Linear(16, 1),
            nn.Sigmoid()
        )

    def forward(self, x):
        return self.layers(x)

    def predict(self, prematch_event):
        fair = prematch_event.get("fair_odds", 1.0)
        tm = prematch_event.get("tippmix_odds", 1.0)

        rel_value = max(0.0, (tm / fair) - 1.0)
        implied_prob = 1 / tm
        fair_prob = 1 / fair
        diff = fair_prob - implied_prob

        x = torch.tensor([rel_value, implied_prob, fair_prob, diff], dtype=torch.float32)
        out = self.forward(x)
        return float(out.item())


# ----------------------------------------------------------
# 2) MomentumHunter AI — Live specialist (xG, shots)
# ----------------------------------------------------------

class MomentumHunterAI(nn.Module):
    def __init__(self):
        super().__init__()
        self.layers = nn.Sequential(
            nn.Linear(6, 32),
            nn.ReLU(),
            nn.Linear(32, 1),
            nn.Sigmoid()
        )

    def forward(self, x):
        return self.layers(x)

    def predict(self, live_event):
        features = np.array([
            live_event.get("xg_home", 0),
            live_event.get("xg_away", 0),
            live_event.get("shots", 0),
            live_event.get("shots_on_target", 0),
            live_event.get("dangerous_attacks", 0),
            live_event.get("momentum", 0.5)
        ], dtype=np.float32)

        out = self.forward(torch.tensor(features))
        return float(out.item())


# ----------------------------------------------------------
# 3) MarketReader AI — Odds movement specialist
# ----------------------------------------------------------

class MarketReaderAI(nn.Module):
    def __init__(self):
        super().__init__()
        self.layers = nn.Sequential(
            nn.Linear(3, 16),
            nn.ReLU(),
            nn.Linear(16, 1),
            nn.Sigmoid()
        )

    def forward(self, x):
        return self.layers(x)

    def predict(self, odds_event):
        prev = odds_event.get("prev_odds", 0)
        cur = odds_event.get("current_odds", 0)

        movement = (prev - cur)
        sharp_signal = 1 if movement > 0.15 else 0
        volatility = abs(movement)

        feats = torch.tensor([movement, sharp_signal, volatility], dtype=torch.float32)
        out = self.forward(feats)
        return float(out.item())


# ----------------------------------------------------------
# 4) RiskMaster AI — stake optimalization expert
# ----------------------------------------------------------

class RiskMasterAI(nn.Module):
    def __init__(self):
        super().__init__()
        self.layers = nn.Sequential(
            nn.Linear(3, 16),
            nn.ReLU(),
            nn.Linear(16, 1),
            nn.Sigmoid()
        )

    def forward(self, x):
        return self.layers(x)

    def predict(self, bankroll, risk_factor, variance):
        features = torch.tensor([
            bankroll,
            risk_factor,
            variance
        ], dtype=torch.float32)

        out = self.forward(features)
        return float(out.item())


# ----------------------------------------------------------
# 5) QuantumSynth — META AI
#    A másik 4 AI eredményét egyesíti.
# ----------------------------------------------------------

class QuantumSynthAI:
    def __init__(self):
        self.weights = {
            "value": 0.35,
            "momentum": 0.30,
            "market": 0.20,
            "risk": 0.15
        }

    def synthesize(self, v, m, mk, r):
        """
        Final AI decision strength.
        """
        final = (
            v * self.weights["value"] +
            m * self.weights["momentum"] +
            mk * self.weights["market"] +
            r * self.weights["risk"]
        )
        return float(final)


# ----------------------------------------------------------
# GLOBAL INSTANCES
# ----------------------------------------------------------

value_ai = ValueFinderAI()
momentum_ai = MomentumHunterAI()
market_ai = MarketReaderAI()
risk_ai = RiskMasterAI()
quantumsynth = QuantumSynthAI()


# ----------------------------------------------------------
# MASTER PREDICTION — a pipeline ezt hívja
# ----------------------------------------------------------

def evaluate_event(prematch=None, live=None, odds=None, bankroll=1000, risk=1.0, variance=0.1):
    """
    Futtatja az összes AI-t, majd összevonja őket.
    """

    v = value_ai.predict(prematch) if prematch else 0.0
    m = momentum_ai.predict(live) if live else 0.0
    mk = market_ai.predict(odds) if odds else 0.0
    r = risk_ai.predict(bankroll, risk, variance)

    final = quantumsynth.synthesize(v, m, mk, r)

    return {
        "value_ai": v,
        "momentum_ai": m,
        "market_ai": mk,
        "risk_ai": r,
        "final_strength": final
    }
