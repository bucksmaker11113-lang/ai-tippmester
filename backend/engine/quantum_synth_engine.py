# ============================================================================
#   QuantumSynthEngine v7.5 ULTRA
#   A teljes Tippmester Quantum Engine központi AI vezérlője
#   Összehangolja:
#       - MonteCarlo v3
#       - GNN csapatháló elemző
#       - LSTM/RNN form-trend predictor
#       - Deep Learning teljesítmény modell
#       - Poisson goal model
#       - RL market adaptation engine
#       - Bookmaker manipulation detector
#       - Value/Bias engine
#       - Kelly bankroll engine
#       - MatchFinder (TippmixPro illesztés)
#       - Single, Kombi, Live tippek
# ============================================================================

import numpy as np
import time

from engine.montecarlo_v3_engine import MonteCarloV3
from engine.gnn_engine import GNNEngine
from engine.lstm_rnn_engine import LSTMEngine
from engine.deep_learning_engine import DeepLearningEngine
from engine.poisson_engine import PoissonEngine
from engine.rl_engine import RLEngine
from engine.bookmaker_engine import BookmakerEngine
from engine.value_engine import ValueEngine
from engine.kelly_engine import KellyEngine
from engine.gameflow_engine import GameflowEngine
from engine.match_finder_engine import MatchFinder

class QuantumSynthEngine:

    def __init__(self):
        self.tippmix_data = []
        self.intl_data = []
        self.aggregated_data = []

        # al-engine példányok
        self.mc = MonteCarloV3()
        self.gnn = GNNEngine()
        self.lstm = LSTMEngine()
        self.dl = DeepLearningEngine()
        self.poisson = PoissonEngine()
        self.rl = RLEngine()
        self.bookmaker = BookmakerEngine()
        self.value = ValueEngine()
        self.kelly = KellyEngine()
        self.gameflow = GameflowEngine()
        self.matchfinder = MatchFinder()

    # ----------------------------------------------------------------------
    # Tippmix adat
    # ----------------------------------------------------------------------
    def set_tippmix_data(self, data):
        self.tippmix_data = data

    # ----------------------------------------------------------------------
    # Belépési pont – teljes odds értékelés
    # ----------------------------------------------------------------------
    def synthesize(self, events):
        """
        A teljes pipeline:
        1) MonteCarlo v3 → raw probability
        2) LSTM form → momentum
        3) GNN → játékos kapcsolati erő
        4) DL → historical performance
        5) Poisson → expected goals
        6) RL → dynamic market weighting
        7) Bookmaker engine → manipulation detection
        8) Value engine → real-value odds
        9) Kelly → stake weight
        """

        processed = []

        for ev in events:

            mc = self.mc.simulate(ev)
            lstm = self.lstm.predict_form(ev)
            gnn = self.gnn.evaluate(ev)
            dl = self.dl.predict_strength(ev)
            px = self.poisson.predict(ev)
            rl = self.rl.adapt(ev)
            bm = self.bookmaker.detect(ev)

            combined_strength = (
                mc * 0.25 +
                lstm * 0.15 +
                gnn * 0.15 +
                dl * 0.15 +
                px * 0.10 +
                rl * 0.10 +
                bm * 0.10
            )

            fair_odds = 1 / max(0.0001, combined_strength)
            real_value = self.value.calculate(ev, fair_odds)
            stake = self.kelly.calculate(real_value, fair_odds)

            processed.append({
                "event": ev,
                "strength": combined_strength,
                "fair_odds": fair_odds,
                "value": real_value,
                "stake": stake
            })

        sorted_events = sorted(processed, key=lambda x: x["value"], reverse=True)
        return sorted_events

    # ----------------------------------------------------------------------
    # TippmixPro illesztése
    # ----------------------------------------------------------------------
    def align_with_tippmix(self, intl_events):
        """
        Ha egy value tipp nincs a TippmixPro-n:
            -> MatchFinder keres helyette megfelelőt
        """
        return self.matchfinder.align(intl_events, self.tippmix_data)

    # ----------------------------------------------------------------------
    # Napi tippek gyártása
    # ----------------------------------------------------------------------
    def generate_daily_tips(self, international_odds):
        """
        Single: 4 tipp (Foci, Kosár, Jégkorong, Tenisz)
        Kombi: 4-5 legerősebb value tipp
        Live: gameflow engine alapján (14:00 után)
        """
        aligned = self.align_with_tippmix(international_odds)
        evaluated = self.synthesize(aligned)

        return evaluated

