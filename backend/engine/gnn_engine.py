# ============================================================================
#   GNN Engine – Tippmester Quantum Engine
#   Könnyített Graph Neural Network modell csapatháló elemzéshez.
#   Nem használ PyTorch/TF-t – helyette numerikus mátrixszintű GNN-szimuláció.
# ============================================================================

import numpy as np
import math
import random


class GNNEngine:

    def __init__(self):
        # grafikus súlymátrix baseline
        self.base_matrix = np.array([
            [1.0, 0.8, 0.7],
            [0.8, 1.0, 0.75],
            [0.7, 0.75, 1.0]
        ])

    # ----------------------------------------------------------------------
    # Csapat relációs mátrix építése
    # ----------------------------------------------------------------------
    def build_graph(self, event):
        """
        A bemenetben várható struktúra:
        event = {
            "team_strength_home": float,
            "team_strength_away": float,
            "mutual_history": float (0–1),
        }
        """

        s_home = event.get("team_strength_home", 0.5)
        s_away = event.get("team_strength_away", 0.5)
        mutual = event.get("mutual_history", 0.5)

        # 3 node: home, away, neutral-context
        matrix = np.array([
            [1.0, s_home, mutual],
            [s_home, 1.0, s_away],
            [mutual, s_away, 1.0]
        ])

        # normalizálás
        matrix = matrix / np.max(matrix)

        return matrix

    # ----------------------------------------------------------------------
    # GNN forward "pesudo-layer"
    # ----------------------------------------------------------------------
    def propagate(self, matrix):
        """
        Könnyített GNN-layer:
        - Mátrix-szorzás self.base_matrix-szal
        - Aktiváció: normál sigmoid
        """
        combined = np.dot(matrix, self.base_matrix)
        activated = 1 / (1 + np.exp(-combined))
        return activated

    # ----------------------------------------------------------------------
    # Kimeneti erősség kiszámítása
    # ----------------------------------------------------------------------
    def evaluate(self, event):
        graph = self.build_graph(event)
        propagated = self.propagate(graph)

        # kimenet → átlagolt „team synergy index”
        synergy = float(np.mean(propagated))

        # skála 0.01 – 0.99
        synergy = max(0.01, min(0.99, synergy))

        return synergy
