from engine.momentum_live import (
    calculate_momentum,
    odds_drop,
    markov_state_transition,
    live_projection
)

from engine.hybridbias import hybrid_bias_live


"""
LIVE ENGINE – Tippmester Quantum Engine
Élő tippek 14:00 után.

Input:
    - live_events: real-time odds feed események
    - minden eseményhez tartozik:
        attack_pressure
        shots
        dangerous_attacks
        possession
        prev_odds
        current_odds
        bayes
        mc_live
        ml_pred
        market_stability
"""


def choose_live_tips(live_events):
    tips = []

    for e in live_events:

        # ------------ MOMENTUM SCORE ------------
        mom = calculate_momentum(
            e.get("attack_pressure", 0),
            e.get("shots", 0),
            e.get("dangerous_attacks", 0),
            e.get("possession", 0)
        )

        # ------------ ODDS DROP ------------
        drop = odds_drop(
            e.get("prev_odds", 0),
            e.get("current_odds", 0)
        )

        # ------------ MARKOV STATE ------------
        markov_s = markov_state_transition(
            e.get("markov_prev", 0.5),
            mom,
            drop
        )

        # ------------ HYBRID LIVE BIAS ------------
        hybrid_live = hybrid_bias_live(
            e.get("bayes", 0.5),
            e.get("mc_live", 0.5),
            e.get("ml_pred", 0.5),
            mom,
            markov_s,
            e.get("market_stability", 1.0)
        )

        # ------------ LIVE PROJECTION ------------
        final_live_strength = live_projection(
            mom,
            markov_s,
            e.get("mc_live", 0.5),
            e.get("market_stability", 1.0)
        )

        # MINIMUM SZŰRÉSEK
        if final_live_strength < 0.60:
            continue
        if hybrid_live < 0.60:
            continue
        if drop < 0.07:  # legalább 7% odds esés kell
            continue

        # kész élő tipp objektum
        tips.append({
            "team1": e.get("team1"),
            "team2": e.get("team2"),
            "sport": e.get("sport"),
            "current_odds": e.get("current_odds"),
            "momentum": mom,
            "markov": markov_s,
            "hybrid_live": hybrid_live,
            "live_strength": final_live_strength
        })

    # ----- Legjobb 2–5 élő tipp visszaadása -----
    tips.sort(key=lambda x: x["live_strength"], reverse=True)

    return tips[:5]   # max 5 élő tipp, minimum 2 ha van elég
