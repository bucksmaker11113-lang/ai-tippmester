# ---------------------------------------------------------
# VALUE SCANNER – Tippmester Quantum Engine
# Több sportágra optimalizálva
# ---------------------------------------------------------

def calculate_edge(tippmix_odds, fair_odds):
    """Edge = (TM odds - fair) / fair"""
    if fair_odds <= 0:
        return 0
    return (tippmix_odds - fair_odds) / fair_odds


def is_value(tippmix_odds, fair_odds):
    """Value szűrő"""
    return tippmix_odds > fair_odds


def market_stability(prev_line, current_line):
    """
    Piaci stabilitás (line movement).
    1.0 → teljesen stabil
    0.0 → széteső piac
    """
    if prev_line == 0:
        return 1.0

    diff = abs(prev_line - current_line) / prev_line
    return max(0.0, min(1.0, 1 - diff))


def sport_weight(sport):
    """
    Sportág súlyozás single tippekhez:
    foci, kosár, hoki, tenisz
    """
    weights = {
        "foci": 0.50,
        "kosar": 0.20,
        "hoki": 0.15,
        "tenisz": 0.15
    }
    return weights.get(sport.lower(), 0.10)


# ---------------------------------------------------------
# FŐ VALUE SZŰRŐ FUNKCIÓ
# ---------------------------------------------------------

def scan_value_events(events):
    """
    Bemenet: events list → minden elem:
    {
        "sport": "foci/kosar/hoki/tenisz",
        "team1": ...,
        "team2": ...,
        "tippmix_odds": 2.15,
        "fair_odds": 1.92,
        "confidence": 0.65,
        "prev_line": 1.85,
        "current_line": 1.90
    }
    """

    result = []

    for e in events:
        fair = e.get("fair_odds", 0)
        tmo = e.get("tippmix_odds", 0)

        # value check
        if not is_value(tmo, fair):
            continue

        edge = calculate_edge(tmo, fair)
        stab = market_stability(e.get("prev_line", 1.0), e.get("current_line", 1.0))
        conf = e.get("confidence", 0.50)
        sport = e.get("sport", "").lower()

        event_data = {
            "sport": sport,
            "team1": e.get("team1"),
            "team2": e.get("team2"),
            "fair_odds": fair,
            "tippmix_odds": tmo,
            "edge": round(edge, 4),
            "confidence": conf,
            "market_stability": stab,
            "sport_weight": sport_weight(sport)
        }

        result.append(event_data)

    return result
