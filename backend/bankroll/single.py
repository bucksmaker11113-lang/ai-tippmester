# SINGLE BANKROLL ENGINE – Tippmester Quantum Engine

bankroll_single = 300000  # alap bankroll például

SPORT_WEIGHT = {
    "foci": (0.41, 0.50),
    "kosar": (0.15, 0.20),
    "hoki": (0.15, 0.20),
    "tenisz": (0.15, 0.25)
}

def get_single_bankroll():
    return bankroll_single

def update_single_bankroll(amount):
    global bankroll_single
    bankroll_single += amount
    return bankroll_single

def calculate_single_stake(sport, strength_score):
    """
    Sportág-arány + strength alapján számított stake.
    Napi teljes risk = bankroll 1%-a.
    """

    total_risk = bankroll_single * 0.01

    w_low, w_high = SPORT_WEIGHT.get(sport, (0.10, 0.10))

    # erős tipp → magasabb súly
    if strength_score >= 0.80:
        w = w_high
    else:
        w = w_low

    return round(total_risk * w, 2)
