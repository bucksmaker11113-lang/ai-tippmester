from engine.hybridbias import hybrid_bias, hybrid_strength

"""
SINGLE ENGINE – Tippmester Quantum Engine
4 sportág → 1-1 tipp minden nap:
- foci
- kosár
- hoki
- tenisz
"""


def choose_best_single_per_sport(value_events):
    """
    value_events = olyan események listája, amik:
    - value_edge
    - confidence
    - fair_odds
    - tippmix_odds
    - sport
    - hybrid inputok: bayes, poisson, mc, ml, market_stability
    """

    best = {
        "foci": None,
        "kosar": None,
        "hoki": None,
        "tenisz": None
    }

    for e in value_events:
        sport = e.get("sport")
        if sport not in best:
            continue

        # HYBRID PROBABILITY
        h_prob = hybrid_bias(
            e.get("bayes", 0.5),
            e.get("poisson_prob", 0.5),
            e.get("mc_prob", 0.5),
            e.get("ml_prob", 0.5),
            e.get("market_stability", 1.0)
        )

        # FINAL STRENGTH
        strength = hybrid_strength(
            e.get("edge", 0),
            h_prob,
            e.get("confidence", 0.5),
            e.get("market_stability", 1.0)
        )

        e["hybrid_prob"] = h_prob
        e["strength"] = strength

        # ha még nincs tipp a sportágnál → ez lesz
        if best[sport] is None:
            best[sport] = e
        else:
            # erősebb tipp cseréli a régit
            if strength > best[sport]["strength"]:
                best[sport] = e

    # visszaadjuk a négy sportból a legjobb egyet-egyet
    result = [best["foci"], best["kosar"], best["hoki"], best["tenisz"]]
    return [x for x in result if x is not None]
