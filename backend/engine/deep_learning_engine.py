# ============================================================================
#   DeepLearningEngine – Tippmester Quantum Engine
#   Egyszerű ANN / DNN modell sportesemény erősségének becslésére.
#   Ez nem deep learning keretrendszerre épül (TensorFlow/PyTorch nélkül),
#   hanem könnyített, gyorsított numerikus neurális háló szimuláció.
# ============================================================================

import numpy as np
import math
import random


class DeepLearningEngine:

    def __init__(self):
        # 3 réteg: input → hidden → output
        self.input_size = 6
        self.hidden_size = 12
        self.output_size = 1

        # súlymátrixok random inicializálása
        self.w1 = np.random.normal(0, 0.15, (self.input_size, self.hidden_size))
        self.w2 = np.random.normal(0, 0.15, (self.hidden_size, self.output_size))

    # ----------------------------------------------------------------------
    # Sigmoid aktiváció
    # ----------------------------------------------------------------------
    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    # ----------------------------------------------------------------------
    # Bemeneti attribútumok felépítése
    # ----------------------------------------------------------------------
    def build_input_vector(self, event):
        # Hard-coded feature set – minimál változat
        return np.array([
            float(event.get("odds", 2.0)),
            float(event.get("rank_diff", 0)),
            float(event.get("form_home", 0.5)),
            float(event.get("form_away", 0.5)),
            float(event.get("motivation", 0.5)),
            float(event.get("fatigue", 0.5)),
        ])

    # ----------------------------------------------------------------------
    # Előrecsorgás (forward pass)
    # ----------------------------------------------------------------------
    def forward(self, x):
        h = self.sigmoid(np.dot(x, self.w1))
        output = self.sigmoid(np.dot(h, self.w2))
        return float(output)

    # ----------------------------------------------------------------------
    # Publikus API: esemény erejének becslése
    # ----------------------------------------------------------------------
    def predict_strength(self, event):
        x = self.build_input_vector(event)
        strength = self.forward(x)

        # skála 0.01 – 0.99 közé
        return max(0.01, min(0.99, strength))
