import random

# ---------------------------------------------------------
# FOCI MONTE CARLO
# ---------------------------------------------------------

def mc_foci(home_strength, away_strength, bias_factor=0.05, sims=20000):
    """
    Foci Monte Carlo – nagy pontosság, 20 000 futás.
    """
    home_win = 0
    for _ in range(sims):
        h = home_strength + random.uniform(-bias_factor, bias_factor)
        a = away_strength + random.uniform(-bias_factor, bias_factor)
        if h > a:
            home_win += 1
    return home_win / sims


# ---------------------------------------------------------
# KOSÁRLABDA MONTE CARLO
# ---------------------------------------------------------

def mc_kosar(home_score, away_score, tempo_factor=0.1, sims=15000):
    """
    Kosárlabda Monte Carlo – 15 000 futás.
    Magas pontszámvariancia miatt dinamikusabb modellel.
    """
    home_win = 0
    for _ in range(sims):
        h = home_score + random.uniform(-tempo_factor, tempo_factor)
        a = away_score + random.uniform(-tempo_factor, tempo_factor)
        if h > a:
            home_win += 1
    return home_win / sims


# ---------------------------------------------------------
# JÉGKORONG MONTE CARLO
# ---------------------------------------------------------

def mc_hoki(goal_strength_home, goal_strength_away, variance=0.15, sims=12000):
    """
    Jégkorong Monte Carlo – 12 000 futás.
    Kisebb gólkülönbségek → nagyobb variancia faktor.
    """
    home_win = 0
    for _ in range(sims):
        h = goal_strength_home + random.uniform(-variance, variance)
        a = goal_strength_away + random.uniform(-variance, variance)
        if h > a:
            home_win += 1
    return home_win / sims


# ---------------------------------------------------------
# TENISZ MONTE CARLO
# ---------------------------------------------------------

def mc_tenis(serve_diff, return_diff, momentum, sims=10000):
    """
    Tenisz Monte Carlo – 10 000 futás.
    Momentum + szervaszázalék + random ingadozás.
    """
    win = 0
    for _ in range(sims):
        score = (
            serve_diff * 0.5 +
            return_diff * 0.3 +
            momentum * 0.2 +
            random.uniform(-0.1, 0.1)
        )
        if score > 0:
            win += 1
    return win / sims
