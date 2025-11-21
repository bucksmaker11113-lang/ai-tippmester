# ---------------------------------------------------------
# HYBRID BIAS ENGINE – Tippmester Quantum Engine
# Összeolvasztja: Bayes + Poisson + MC + ML + Value + Market
# ---------------------------------------------------------

def hybrid_bias(
    bayes_prob: float,
    poisson_prob: float,
    mc_prob: float,
    ml_prob: float,
    market_stability: float
):
    """
    Alap hibrid bias motor (pre-match tippekhez).
    Súlyozás a Tippmester Quantum Engine szabvány alapján.
    """

    final = (
        0.30 * bayes_prob +
        0.25 * poisson_prob +
        0.25 * mc_prob +
        0.15 * ml_prob +
        0.05 * market_stability
    )

    # clamp 0–1 között
    return max(0.0, min(1.0, final))


# ---------------------------------------------------------
# HYBRID BIAS – ÉLŐ TIPPEKRE
# Markov + Momentum is bevesz
# ---------------------------------------------------------

def hybrid_bias_live(
    bayes_prob: float,
    mc_live_prob: float,
    ml_prob: float,
    momentum: float,
    markov_state: float,
    market_stability: float
):
    """
    Hibrid élő bias modell – momentum + Markov súlyokkal.
    """

    final = (
        0.25 * bayes_prob +
        0.25 * mc_live_prob +
        0.20 * ml_prob +
        0.15 * momentum +
        0.10 * markov_state +
        0.05 * market_stability
    )

    return max(0.0, min(1.0, final))


# ---------------------------------------------------------
# HYBRID STRENGTH SCORE (single, kombi, live kiválasztáshoz)
# ---------------------------------------------------------

def hybrid_strength(value_edge, hybrid_prob, confidence, market_sharp):
    """
    Egységes erősségi score – ezt használjuk:
    - single tipp kiválasztás
    - kombi tipp kiválasztás
    - élő tipp validáció
    """

    score = (
        0.40 * value_edge +
        0.30 * hybrid_prob +
        0.20 * confidence +
        0.10 * market_sharp
    )

    return round(score, 4)
