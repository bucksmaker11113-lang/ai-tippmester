# ---------------------------------------------------------
# BAYES ALAP FÜGGVÉNYEK
# ---------------------------------------------------------

def bayes_update(prior, likelihood, evidence):
    """
    Egyszerű Bayes-frissítés.
    P(A|B) = (P(B|A) * P(A)) / P(B)
    """
    if evidence == 0:
        return prior
    return (likelihood * prior) / evidence


# ---------------------------------------------------------
# FOCI BAYES-MODELL
# ---------------------------------------------------------

def bayes_foci(form_rating, home_advantage, market_strength):
    """
    Foci Bayes:
    - prior = forma rating (0–1)
    - likelihood = hazai előny (hazai csapat esetén)
    - evidence = piac ereje (closing line)
    """

    prior = form_rating
    likelihood = home_advantage
    evidence = max(0.01, market_strength)

    post = bayes_update(prior, likelihood, evidence)

    return max(0.01, min(0.99, post))  # clamp 0–1 range


# ---------------------------------------------------------
# KOSÁRLABDA BAYES-MODELL
# ---------------------------------------------------------

def bayes_kosar(team_power, pace_factor, line_consistency):
    """
    Kosárlabda:
    - prior = csapat ereje
    - likelihood = pace hatás
    - evidence = line stabilitása
    """

    prior = team_power
    likelihood = pace_factor
    evidence = max(0.01, line_consistency)

    post = bayes_update(prior, likelihood, evidence)

    return max(0.01, min(0.99, post))


# ---------------------------------------------------------
# JÉGKORONG BAYES-MODELL
# ---------------------------------------------------------

def bayes_hoki(shots_for, shots_against, goalie_factor):
    """
    Hoki Bayes:
    - prior = lövéskülönbség
    - likelihood = kapusteljesítmény
    - evidence = kapott gól képesség
    """

    prior = shots_for / max(1, shots_for + shots_against)
    likelihood = goalie_factor
    evidence = max(0.01, (shots_against / 100) + 0.1)

    post = bayes_update(prior, likelihood, evidence)

    return max(0.01, min(0.99, post))


# ---------------------------------------------------------
# TENISZ BAYES-MODELL
# ---------------------------------------------------------

def bayes_tenis(first_serve_pct, return_points, fatigue_factor):
    """
    Tenisz Bayes:
    - prior = első szerva %-a
    - likelihood = return point win%
    - evidence = fáradtság faktor
    """

    prior = first_serve_pct
    likelihood = return_points
    evidence = max(0.01, fatigue_factor)

    post = bayes_update(prior, likelihood, evidence)

    return max(0.01, min(0.99, post))
