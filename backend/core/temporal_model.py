"""
Temporal Model – Idősoros tanulás
"""

import numpy as np
import pandas as pd
from datetime import datetime

class TemporalModel:
    def __init__(self):
        self.data = pd.DataFrame(columns=["timestamp", "team_a", "team_b", "value"])

    def add_entry(self, team_a, team_b, value):
        self.data.loc[len(self.data)] = [datetime.now(), team_a, team_b, value]

    def get_recent_trend(self, team):
        """Egyszerű mozgóátlag trend"""
        subset = self.data[(self.data["team_a"] == team) | (self.data["team_b"] == team)]
        if len(subset) < 3:
            return 0.0
        return subset["value"].tail(5).mean() - subset["value"].head(5).mean()
