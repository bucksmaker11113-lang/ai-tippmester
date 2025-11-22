"""
Bankroll Analytics – Tippmester AI Fusion 1.0
ROI és statisztikai kimutatások.
"""

import pandas as pd

class BankrollAnalytics:
    def __init__(self, csv_path="backend/data/bankroll_profiles.csv"):
        self.path = csv_path

    def calculate_roi(self):
        try:
            df = pd.read_csv(self.path)
            start_balance = df["balance"].iloc[0]
            end_balance = df["balance"].iloc[-1]
            return round(((end_balance - start_balance) / start_balance) * 100, 2)
        except Exception:
            return 0.0

