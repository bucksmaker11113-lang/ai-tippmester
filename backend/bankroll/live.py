# LIVE BANKROLL ENGINE – Tippmester Quantum Engine

bankroll_live = 300000

def get_live_bankroll():
    return bankroll_live

def update_live_bankroll(amount):
    global bankroll_live
    bankroll_live += amount
    return bankroll_live

def calculate_live_stake(live_strength, momentum):
    """
    Élő tipp stake:
    - live_strength: 0.0–1.0
    - momentum: 0.0–1.0
    """

    # napi risk 0.5%–2%
    low = bankroll_live * 0.005
    mid = bankroll_live * 0.01
    high = bankroll_live * 0.02

    if live_strength >= 0.80 and momentum >= 0.70:
        return round(high, 2)

    if live_strength >= 0.65:
        return round(mid, 2)

    return round(low, 2)
