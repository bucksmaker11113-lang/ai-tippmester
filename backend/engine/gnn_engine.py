# ==============================================================================
#   GRAPH ANALYTIC ENGINE (GNN-LITE) – Tippmester Quantum Engine 7.0
# ------------------------------------------------------------------------------
# Sporttaktikai hálózatelemzés:
#   - passz/shot network
#   - dangerous attack connectivity
#   - team shape stability
#   - key player nodes
#   - pressure graph
#
# Ad ki:
#   "tactical_strength": 0–1
#   "shape_stability": 0–1
#   "pressure_index": 0–1
# ==============================================================================

import numpy as np

class GNNEdgeEngine:

    def __init__(self):
        pass

    # ---------------------------------------------------------
    # Egyszerű node centrality számítás
    # ---------------------------------------------------------
    def node_centrality(self, edges):
        if len(edges) == 0:
            return 0.1
        strengths = [w for (_, _, w) in edges]
        return float(np.clip(np.mean(strengths), 0.05, 1.0))

    # ---------------------------------------------------------
    # Formáció stabilitás
    # ---------------------------------------------------------
    def shape_stability(self, formation_changes):
        if len(formation_changes) == 0:
            return 0.5
        change_rate = np.mean(formation_changes)
        stab = 1 - np.clip(change_rate, 0, 1)
        return float(np.clip(stab, 0.1, 0.95))

    # ---------------------------------------------------------
    # Pressing háló index
    # ---------------------------------------------------------
    def pressure_index(self, duels_won, turnovers_forced):
        base = (np.mean(duels_won) * 0.6 + np.mean(turnovers_forced) * 0.4) / 100
        return float(np.clip(base, 0.05, 1.0))

    # ---------------------------------------------------------
    # FŐ HÁLÓZATI TÁMADÁS / TÁMADÓ ERŐ
    # ---------------------------------------------------------
    def tactical_strength(self, pass_edges, shot_edges, danger_edges):
        nodes = pass_edges + shot_edges + danger_edges
        if len(nodes) == 0:
            return 0.1
        vals = [w for (_, _, w) in nodes]
        return float(np.clip(np.mean(vals), 0.05, 1.0))

    # ---------------------------------------------------------
    # FŐ GNN-LITE PREDIKCIÓ
    # ---------------------------------------------------------
    def analyze_graph(self, team_graph):
        """
        team_graph:
            {
                "pass_edges": [(a,b,w), ...],
                "shot_edges": [(a,b,w), ...],
                "danger_edges": [(a,b,w), ...],
                "formation_changes": [...],
                "duels_won": [...],
                "turnovers_forced": [...]
            }
        """

        pass_edges = team_graph.get("pass_edges", [])
        shot_edges = team_graph.get("shot_edges", [])
        danger_edges = team_graph.get("danger_edges", [])

        shape = self.shape_stability(team_graph.get("formation_changes", []))
        press = self.pressure_index(
            team_graph.get("duels_won", [0]),
            team_graph.get("turnovers_forced", [0])
        )
        tactical = self.tactical_strength(pass_edges, shot_edges, danger_edges)

        return {
            "tactical_strength": float(tactical),
            "shape_stability": float(shape),
            "pressure_index": float(press),
            "gnn_score": float(np.clip(
                tactical * 0.6 + shape * 0.2 + press * 0.2,
                0.05, 1.0
            ))
        }


# GLOBAL INSTANCE
gnn_engine = GNNEdgeEngine()
