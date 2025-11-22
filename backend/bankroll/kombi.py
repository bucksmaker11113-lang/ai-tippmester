# KOMBI BANKROLL ENGINE – Tippmester Quantum Engine

bankroll_kombi = 300000  # alap bankroll

def get_kombi_bankroll():
    return bankroll_kombi

def update_kombi_bankroll(amount):
    global bankroll_kombi
    bankroll_kombi += amount
    return bankroll_kombi

def calculate_kombi_stake(kombi_strength):
    """
    Kombi tipp stake számítása:
    - kombi_strength = az 5 tipp átlag strength értéke
    """

    # napi 0.5%–1% risk
    low = bankroll_kombi * 0.005
    high = bankroll_kombi * 0.01

    if kombi_strength >= 0.75:
        return round(high, 2)
    else:
        return round(low, 2)
