"""
Bankroll Manager – Tippmester 5.2
Többprofilos bankroll kezelő, kockázat-alapú elosztással.
"""

import csv
from datetime import datetime

class BankrollManager:
    def __init__(self, bankroll=300000, risk_mode="balanced"):
        self.start_bankroll = bankroll
        self.balance = bankroll
        self.risk_mode = risk_mode
        self.history = []

    def place_bet(self, odds, confidence):
        """Kiszámolja a tétet a bizalom és a kockázati mód alapján."""
        base_percent = {"safe": 0.005, "balanced": 0.01, "aggressive": 0.02}
        bet_percent = base_percent.get(self.risk_mode, 0.01)
        stake = round(self.balance * bet_percent * confidence, 2)
        return min(stake, self.balance)

    def update_balance(self, stake, odds, result):
        """Frissíti a bankrollt a tipp eredménye alapján."""
        if result == "win":
            profit = stake * (odds - 1)
            self.balance += profit
        elif result == "loss":
            self.balance -= stake

        self.history.append({
            "date": datetime.now().isoformat(),
            "result": result,
            "stake": stake,
            "balance": self.balance
        })

    def export_history(self, filepath="backend/data/bankroll_profiles.csv"):
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=self.history[0].keys())
            writer.writeheader()
            writer.writerows(self.history)
