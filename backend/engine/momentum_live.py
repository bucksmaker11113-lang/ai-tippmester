import random
import math


# ---------------------------------------------------------
# MOMENTUM ENGINE (élő tippekhez)
# ---------------------------------------------------------

def calculate_momentum(attack_pressure, shots, dangerous_attacks, possession):
    """
    Támadásnyomás, kapura lövések, veszélyes támadások,
    labdabirtoklás összegzett momentum értéke.
    """

    momentum = (
        0.35 * attack_pressure +
        0.30 * shots +
        0.20 * dangerous_attacks +
        0.15 * possession
    )

    # normalizált 0–1 skálára
    return max(0.0, min(1.0, momentum))


# ---------------------------------------------------------
# ODDS DROP DETECTOR (élő piac figyelése)
# ---------------------------------------------------------

def odds_drop(prev_odds, current_odds):
    """
    Odds esés detektálása.
    """
    if prev_odds == 0:
        return 0

    drop = (prev_odds - current_odds) / prev_odds
    return max(0, drop)


# ---------------------------------------------------------
# MARKOV-LIVE ENGINE (állapotátmenetek)
# ---------------------------------------------------------

def markov_state_transition(current_state, momentum, odds_drop_val):
    """
    A Markov Live Engine a következő állapotot becsüli.
    """
    transition_value = (
        0.5 * momentum +
        0.3 * odds_drop_val +
        0.2 * current_state +
        random.uniform(-0.05, 0.05)
    )

    return max(0.0, min(1.0, transition_value))


# ---------------------------------------------------------
# ÉLŐ PROJEKCIÓ (összegzett valószínűség)
# ---------------------------------------------------------

def live_projection(momentum, markov_state, mc_live_prob, market_stability):
    """
    Élő tipp végső erőssége.
    """

    final_strength = (
        0.4 * momentum +
        0.3 * markov_state +
        0.2 * mc_live_prob +
        0.1 * market_stability
    )

    return max(0.0, min(1.0, final_strength))
