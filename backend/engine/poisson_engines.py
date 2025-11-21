import math

# ---------------------------------------------------------
# FOCI POISSON GÓLMODELL
# ---------------------------------------------------------

def poisson_probability(goals, lambda_val):
    return (lambda_val ** goals) * math.exp(-lambda_val) / math.factorial(goals)


def poisson_foci(avg_home_goals, avg_away_goals, max_goals=6):
    """
    Foci Poisson – várható gólokból valószínűségi mátrix.
    """
    matrix = []
    for h in range(max_goals + 1):
        for a in range(max_goals + 1):
            p = poisson_probability(h, avg_home_goals) * \
                poisson_probability(a, avg_away_goals)
            matrix.append({"home": h, "away": a, "prob": p})
    return matrix


# ---------------------------------------------------------
# JÉGKORONG POISSON – kevesebb gól, kisebb lambda
# ---------------------------------------------------------

def poisson_hoki(avg_home, avg_away, max_goals=5):
    matrix = []
    for h in range(max_goals + 1):
        for a in range(max_goals + 1):
            p = poisson_probability(h, avg_home) * \
                poisson_probability(a, avg_away)
            matrix.append({"home": h, "away": a, "prob": p})
    return matrix


# ---------------------------------------------------------
# KOSÁRLABDA "POISSON-SZERŰ" SCORING MODEL
# (nem klasszikus Poisson, mert túl sok pont → scaling + distribution shift)
# ---------------------------------------------------------

def poisson_kosar(avg_home, avg_away):
    """
    A kosárlabda terheléshez Poisson helyett
    skálázott approximációt használunk.
    """
    return {
        "projection_home": avg_home + (avg_home * 0.03),
        "projection_away": avg_away + (avg_away * 0.03)
    }


# ---------------------------------------------------------
# TENISZ POISSON – "point-win-rate" modellezéshez
# ---------------------------------------------------------

def poisson_tenis(serve_win_rate, return_win_rate):
    """
    Tenisz Poisson-szerű modell: várható game-nyerési esély.
    """
    serve_project = serve_win_rate * 0.65
    return_project = return_win_rate * 0.35

    return {
        "serve_projection": serve_project,
        "return_projection": return_project
    }
