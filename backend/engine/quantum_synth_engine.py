# ==============================================================================
#                 QUANTUM SYNTH ENGINE – Quantum Engine 7.5 ULTRA
# ------------------------------------------------------------------------------
# A világ egyik legerősebb sportfogadási többmotoros AI rendszere:
#
#   - Monte Carlo Engine v2
#   - Hybrid Bias Engine
#   - Bayesian Rating Layer
#   - LSTM/RNN Next Goal Engine
#   - GameFlow Engine
#   - Kelly bankroll optimalizáló
#   - GNN Tactical Engine
#   - Bookmaker Agent Reaction Engine
#   - TippmixPro Matching Engine (value replacement logic)
#
# FŐ FUNKCIÓK:
#   ✓ Single tippek (4 sport)
#   ✓ Kombi (4–5 value tip)
#   ✓ Élő tippek (LSTM + GameFlow)
#   ✓ TippmixPro oddsra optimalizálás
#   ✓ Ha egy value tipp nincs a TippmixPron → automatikus pótlás
#
# ==============================================================================

import numpy as np

from engine.monte_carlo_engine import mc_engine
from engine.bias_engine import bias_engine
from engine.bayesian_engine import bayes_engine
from engine.gameflow_engine import gameflow_engine
from engine.lstm_rnn_engine import lstm_rnn_engine
from engine.kelly_engine import kelly_engine
from engine.gnn_engine import gnn_engine
from engine.bookmaker_agent_engine import bookmaker_agent
from engine.tippmixpro_engine import tippmix_engine


class QuantumSynthEngine:

    def __init__(self):
        self.bankrolls = {
            "single": 300000,
            "kombi": 300000,
            "live": 300000
        }

        self.sport_weights = {
            "foci": 0.40,
            "kosar": 0.25,
            "hok": 0.20,
            "tenisz": 0.15
        }

    # ==========================================================================
    # VALUE + TIPPMIXPRO FILTER + VALUE REPLACEMENT
    # ==========================================================================

    def filter_tippmixpro(self, value_events):
        """
        value_events = nemzetközi value tippek
        visszaadja:
            - csak TippmixPro-ban megtalált eventeket
            - Tippmix odds-szal
        a többinél → helyettesítés
        """
        confirmed = []

        for ev in value_events:
            tm = tippmix_engine.find_match(ev)

            if tm["found"]:
                # TippmixPro odds felülírja a nemzetközi oddst
                ev["odds"] = tm["odds"]
                confirmed.append(ev)

        return confirmed

    # ==========================================================================
    # AI SCORE: Monte Carlo → Bias → Bayesian → GNN → Agent → Final score
    # ==========================================================================

    def calculate_strength(self, event):

        # 1) Monte Carlo baseline
        mc_score = mc_engine.simulate_event(event)

        # 2) Bias correction
        bias_score = bias_engine.apply_bias(event, mc_score)

        # 3) Bayesian fusion
        bayes_score = bayes_engine.combine(mc_score, bias_score)

        # 4) GNN tactical analysis
        gnn_score = gnn_engine.analyze_graph(event.get("team_graph", {}))

        # 5) Market reaction
        agent_score = bookmaker_agent.analyze_market(
            event.get("odds_history", []),
            event.get("market_volume", 0),
            event.get("market_volatility", 0)
        )

        # 6) Sport súly
        sw = self.sport_weights.get(event.get("sport", "foci"), 0.2)

        # 7) FINAL AGGREGATED SCORE
        final = (
            bayes_score * 0.45 +
            gnn_score["gnn_score"] * 0.25 +
            agent_score["agent_score"] * 0.15 +
            sw * 0.15
        )

        return {
            "mc": mc_score,
            "bias": bias_score,
            "bayes": bayes_score,
            "gnn": gnn_score,
            "agent": agent_score,
            "final": float(np.clip(final, 0.01, 0.99))
        }

    # ==========================================================================
    # VALUE DETECTION (INTERNATIONAL ODDS)
    # ==========================================================================

    def is_value(self, score, odds):
        fair_odds = 1 / score
        return odds > fair_odds

    # ==========================================================================
    # SINGLE TIPS: 1 foci, 1 kosár, 1 hoki, 1 tenisz
    # ==========================================================================

    def generate_single_tips(self, events):

        # 1) Nemzetközi value tippek kiszűrése
        value_candidates = []
        for ev in events:
            s = self.calculate_strength(ev)
            if self.is_value(s["final"], ev["odds"]):
                ev["ai_score"] = s
                value_candidates.append(ev)

        # 2) TippmixPro szűrés → helyettesítés
        value_tippmix = self.filter_tippmixpro(value_candidates)

        # 3) Sport szerinti rendezés
        buckets = { "foci": [], "kosar": [], "hok": [], "tenisz": [] }

        for ev in value_tippmix:
            buckets[ev["sport"]].append(ev)

        result = []

        # 4) Mindig legyen 1 db minden sportból
        for sp in buckets:
            if not buckets[sp]:
                continue

            best = sorted(
                buckets[sp],
                key=lambda x: x["ai_score"]["final"],
                reverse=True
            )[0]

            stake = kelly_engine.allocate(
                bankrolls=self.bankrolls,
                tip_type="single",
                odds=best["odds"],
                win_prob=best["ai_score"]["final"]
            )

            best["stake"] = stake
            result.append(best)

        return result

    # ==========================================================================
    # KOMBI TIPPEK – Always 4–5 Tippmix-pro-confirmed value
    # ==========================================================================

    def generate_kombi_tip(self, events):

        # Nemzetközi value
        value_candidates = []
        for ev in events:
            s = self.calculate_strength(ev)
            if self.is_value(s["final"], ev["odds"]):
                ev["ai_score"] = s
                value_candidates.append(ev)

        # TippmixPro matched only
        value_tm = self.filter_tippmixpro(value_candidates)

        if len(value_tm) < 4:
            return None

        # 4–5 top tipp
        picks = sorted(
            value_tm,
            key=lambda x: x["ai_score"]["final"],
            reverse=True
        )[:5]

        combined_odds = 1
        combined_prob = 1

        for p in picks:
            combined_odds *= p["odds"]
            combined_prob *= p["ai_score"]["final"]

        stake = kelly_engine.allocate(
            bankrolls=self.bankrolls,
            tip_type="kombi",
            odds=combined_odds,
            win_prob=combined_prob
        )

        return {
            "tips": picks,
            "combined_odds": combined_odds,
            "combined_prob": combined_prob,
            "stake": stake
        }

    # ==========================================================================
    # LIVE TIP – LSTM / GameFlow / Kelly
    # ==========================================================================

    def generate_live_tip(self, live_stats, odds):

        gf = gameflow_engine.predict_next_gameflow(live_stats)

        goal_chance = gf["goal_chance"]

        # value élőben
        if odds <= 1 / goal_chance:
            return None

        stake = kelly_engine.allocate(
            bankrolls=self.bankrolls,
            tip_type="live",
            odds=odds,
            win_prob=goal_chance
        )

        return {
            "match": live_stats.get("match"),
            "odds": odds,
            "stake": stake,
            "goal_chance": goal_chance,
            "confidence": gf["confidence"],
            "live_prediction": gf
        }


# GLOBAL INSTANCE
quantum_synth = QuantumSynthEngine()
