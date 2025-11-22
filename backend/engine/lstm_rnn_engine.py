# ============================================================================
#   LSTM / RNN Engine – Tippmester Quantum Engine
#   Könnyített rekurzív forma-előrejelző modell (LSTM-szerű működés)
#   Idősor alapú teljesítménybecslés csapatokra / játékosokra.
# ============================================================================

import numpy as np
import random
import math


class LSTMEngine:

    def __init__(self):
        # belső állapot
        self.hidden_state = 0.5
        self.cell_state = 0.5

        # tanulási paraméterek
        self.forget_weight = 0.65
        self.input_weight = 0.55
        self.output_weight = 0.60

    # ----------------------------------------------------------------------
    # Aktivációk
    # ----------------------------------------------------------------------
    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def tanh(self, x):
        return np.tanh(x)

    # ----------------------------------------------------------------------
    # Forma-idősor felépítése
    # ----------------------------------------------------------------------
    def build_sequence(self, event):
        """
        Az input várható szerkezete:
            - utolsó 5 meccs eredménye (1/0)
            - átlagos gólkülönbség
            - momentum index (0–1)
        """
        seq = event.get("form_sequence", [1, 0, 1, 1, 0])

        if len(seq) < 5:
            seq = seq + [0] * (5 - len(seq))

        goal_diff = event.get("avg_goal_diff", 0.0)
        momentum = event.get("momentum", 0.5)

        return np.array(seq + [goal_diff, momentum])

    # ----------------------------------------------------------------------
    # LSTM előrecsorgás (befogadó kapu → felejtő kapu → kimeneti kapu)
    # ----------------------------------------------------------------------
    def forward(self, x):
        # forget gate
        forget_gate = self.sigmoid(np.mean(x) * self.forget_weight)

        # input gate
        input_gate = self.sigmoid(np.mean(x) * self.input_weight)

        # candidate value
        candidate = self.tanh(np.mean(x))

        # frissített cell state
        self.cell_state = forget_gate * self.cell_state + input_gate * candidate

        # output gate
        output_gate = self.sigmoid(np.mean(x) * self.output_weight)

        # hidden state
        self.hidden_state = output_gate * self.tanh(self.cell_state)

        return float(self.hidden_state)

    # ----------------------------------------------------------------------
    # Publikus API
    # ----------------------------------------------------------------------
    def predict_form(self, event):
        seq = self.build_sequence(event)
        prediction = self.forward(seq)

        # skálázás
        prediction = max(0.01, min(0.99, prediction))

        return prediction
