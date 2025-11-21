import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np

from database.db import SessionLocal
from database.models import OddsHistory, LiveStatsHistory, TipSingle, TipLive


# ------------------------------------------------------
# 1) FEATURE BUILDER
# ------------------------------------------------------

def build_features(limit=2000):
    """
    Odds history + live stats + tipp outcome alignment
    A rendszer ebből fog tanulni.
    """

    db = SessionLocal()

    odds = db.query(OddsHistory).order_by(OddsHistory.id.desc()).limit(limit).all()
    stats = db.query(LiveStatsHistory).order_by(LiveStatsHistory.id.desc()).limit(limit).all()

    X = []
    y = []

    for o in odds:
        # Odds változás (drop)
        drop = -1
        if o.odds > 0:
            drop = o.odds

        # A statokból
        st = stats[np.random.randint(len(stats))].stats if stats else {}

        # Feature vektor összeállítása
        feats = [
            float(drop),
            float(st.get("shots", 0)),
            float(st.get("shots_on_target", 0)),
            float(st.get("dangerous_attacks", 0)),
            float(st.get("xg_home", 0)),
            float(st.get("xg_away", 0)),
            float(st.get("momentum", 0.5))
        ]

        # Label → a rendszer jelenlegi erősség előrejelzése
        # (később eredményre is tanítható)
        y.append(np.clip(st.get("momentum", 0.5), 0, 1))

        X.append(feats)

    X = np.array(X, dtype=np.float32)
    y = np.array(y, dtype=np.float32)

    if len(X) < 10:
        return None, None

    return X, y.reshape(-1, 1)


# ------------------------------------------------------
# 2) NEURÁLIS HÁLÓ
# ------------------------------------------------------

class DeepLearningModel(nn.Module):
    def __init__(self, input_dim=7):
        super().__init__()
        self.layers = nn.Sequential(
            nn.Linear(input_dim, 32),
            nn.ReLU(),
            nn.Linear(32, 16),
            nn.ReLU(),
            nn.Linear(16, 1),
            nn.Sigmoid()
        )

    def forward(self, x):
        return self.layers(x)


model = DeepLearningModel()
optimizer = optim.Adam(model.parameters(), lr=0.001)
loss_fn = nn.MSELoss()


# ------------------------------------------------------
# 3) TRAINING LOOP
# ------------------------------------------------------

def train_model():
    X, y = build_features()

    if X is None:
        print("[DL] Nincs elég adat a tanuláshoz.")
        return

    X = torch.tensor(X)
    y = torch.tensor(y)

    for epoch in range(20):
        pred = model(X)
        loss = loss_fn(pred, y)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    print(f"[DL] Tanulás kész. Loss={loss.item():.4f}")


# ------------------------------------------------------
# 4) PREDIKCIÓ A PIPELINE-NÉL
# ------------------------------------------------------

def predict_strength(event):
    """
    Egy esemény statjaiból és oddsából előrejelzi:
    Mennyire erős a tipp valójában? (0–1)
    """

    feats = np.array([
        float(event.get("current_odds", 1.5)),
        float(event.get("shots", 0)),
        float(event.get("shots_on_target", 0)),
        float(event.get("dangerous_attacks", 0)),
        float(event.get("xg_home", 0)),
        float(event.get("xg_away", 0)),
        float(event.get("momentum", 0.5)),
    ], dtype=np.float32)

    inp = torch.tensor(feats).unsqueeze(0)
    out = model(inp)

    return float(out.item())


# ------------------------------------------------------
# 5) SELF-TRAIN FUNKCIÓ (naponta 1x)
# ------------------------------------------------------

def auto_self_training():
    try:
        train_model()
    except:
        pass
