import numpy as np
import random
from datetime import datetime

class MonteCarloEngine:
    def __init__(self, bankroll=300000, simulations=10000):
        self.bankroll = bankroll
        self.simulations = simulations
        self.results = []

    def simulate(self, odds, win_prob):
        for _ in range(self.simulations):
            outcome = random.random() < win_prob
            profit = (odds - 1) * 100 if outcome else -100
            self.results.append(profit)
        return np.mean(self.results), np.std(self.results)

    def recommend(self, odds_list, probs):
        recommendations = []
        for i, odds in enumerate(odds_list):
            mean, std = self.simulate(odds, probs[i])
            ev = mean - std / 2
            recommendations.append({
                "odds": odds,
                "prob": probs[i],
                "expected_value": round(ev, 2)
            })
        best = max(recommendations, key=lambda x: x["expected_value"])
        return {"best_pick": best, "details": recommendations}
