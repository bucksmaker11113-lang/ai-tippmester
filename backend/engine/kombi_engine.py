from engine.hybridbias import hybrid_bias, hybrid_strength


"""
KOMBI ENGINE – Tippmester Quantum Engine
4–5 darab erős value tippet választ:
- odds kb. 1.80–2.20
- edge >= 6%
- confidence >= 0.60
- hybrid_bias >= 0.60
- SOHA nem lehet benne a single tippek közül átvett esemény
"""


def filter_out_single_events(value_events, single_events):
    """
    Kiveszi azokat az eseményeket, amik a single tippekben már szerepeltek.
    """
    filtered = []

    for e in value_events:
        is_duplicate = False
        for s in single_events:
            if (
                e.get("team1") == s.get("team1") and
                e.get("team2") == s.get("team2")
            ):
                is_duplicate = True
                break

        if not is_duplicate:
            filtered.append(e)

    return filtered


def choose_kombi_tips(value_events, single_events):
    """
    Kombi tipp logika:
    1) kiszűri a single duplikációkat
    2) értékeli az eseményeket
    3) 4–5 legerősebb tipp kiválasztása
    """

    # ----- 1) SINGLE DUPLIKÁCIÓK KISZŰRÉSE -----
    candidates = filter_out_single_events(value_events, single_events)

    scored = []

    for e in candidates:

        # odds követelmény (~2.0)
        tmo = e.get("tippmix_odds", 0)
        if tmo < 1.80 or tmo > 2.20:
            continue

        # gyenge value ne kerüljön be
        if e.get("edge", 0) < 0.06:
            continue
        if e.get("confidence", 0.5) < 0.60:
            continue

        # HYBRID PROBABILITY számítás
        h_prob = hybrid_bias(
            e.get("bayes", 0.5),
            e.get("poisson_prob", 0.5),
            e.get("mc_prob", 0.5),
            e.get("ml_prob", 0.5),
            e.get("market_stability", 0.5)
        )

        if h_prob < 0.60:
            continue

        # végső strength score
        strength = hybrid_strength(
            e.get("edge"),
            h_prob,
            e.get("confidence"),
            e.get("market_stability")
        )

        e["hybrid_prob"] = h_prob
        e["strength"] = strength

        scored.append(e)

    # ----- 2) SORTOLÁS – legerősebb tipp elöl -----
    scored.sort(key=lambda x: x["strength"], reverse=True)

    # ----- 3) 4–5 KIVÁLASZTÁSA -----
    if len(scored) <= 4:
        return scored[:4]     # ha kevés van, 4 tipp kötelező

    return scored[:5]         # ideális: 5 tipp
