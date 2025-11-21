import numpy as np

# ---------------------------------------------------------
# ML ENGINE ALAP (BETÖLTÉS + NORMALIZÁLÁS)
# ---------------------------------------------------------

class MLModel:
    """
    Általános ML modell wrapper (XGBoost / LightGBM / ANN).
    load_model(path) → betölti a modellt
    predict(features) → visszaadja az 0–1 valószínűséget
    """

    def __init__(self):
        self.model = None

    def load_model(self, model):
        """Külső ML modell objektum beállítása"""
        self.model = model

    def predict(self, features: list):
        if self.model is None:
            return 0.5  # fallback ha nincs modell betöltve
        X = np.array([features], dtype=float)
        return float(self.model.predict_proba(X)[0][1])


# ---------------------------------------------------------
# FOCI ML ENGINE
# ---------------------------------------------------------

def ml_foci(form, attack, defense, possession, shots_on_goal):
    features = [
        form,
        attack,
        defense,
        possession,
        shots_on_goal
    ]

    # itt ML modell csatlakozik → fallback 0.55
    return 0.55


# ---------------------------------------------------------
# KOSÁRLABDA ML ENGINE
# ---------------------------------------------------------

def ml_kosar(pace, offensive_rating, defensive_rating, turnovers, rebounds):
    features = [
        pace,
        offensive_rating,
        defensive_rating,
        turnovers,
        rebounds
    ]

    return 0.57


# ---------------------------------------------------------
# HOKI ML ENGINE
# ---------------------------------------------------------

def ml_hoki(shots_for, shots_against, ppg, pk, goalie_rating):
    features = [
        shots_for,
        shots_against,
        ppg,
        pk,
        goalie_rating
    ]

    return 0.56


# ---------------------------------------------------------
# TENISZ ML ENGINE
# ---------------------------------------------------------

def ml_tenis(first_serve_pct, aces, double_faults, winners, errors):
    features = [
        first_serve_pct,
        aces,
        double_faults,
        winners,
        errors
    ]

    return 0.58
