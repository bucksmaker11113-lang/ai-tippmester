"""
MonteCarlo Engine – Tippmester AI Fusion 1.0
Monte Carlo alapú value odds szimuláció és predikció.
Használat: a ValueAnalyzer hívja meg párhuzamos szálban.
"""

import random
import math
from datetime import datetime


class MonteCarloEngine:
    def __init__(self, simulations=1000):
        self.simulations = simulations

    def run_simulation(self, match):
        """
        Egyetlen mérkőzésre lefuttat egy Monte Carlo szimulációt.
        A cél: győzelmi valószínűség és várható odds becslés.
        """
        try:
            # Dummy alapadatok – a jövőben adatbázisból vagy API-ból jönnek
            home_strength = random.uniform(0.4, 0.7)
            away_strength = random.uniform(0.3, 0.6)

            home_wins = 0
            for _ in range(self.simulations):
                h_score = random.gauss(home_strength * 3, 1.0)
                a_score = random.gauss(away_strength * 3, 1.0)
                if h_score > a_score:
                    home_wins += 1

            win_probability = home_wins / self.simulations
            odds = round(1 / max(win_probability, 0.05), 2)

            return {
                "match": match,
                "win_probability": round(win_probability, 3),
                "odds": odds,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

        except Exception as e:
            return {
                "match": match,
                "error": str(e),
                "win_probability": 0.5,
                "odds": 2.0
            }

    def find_value_odds(self, matches):
        """
        Több mérkőzésre futtatja a Monte Carlo szimulációkat,
        és visszaadja a Tippmester „saját” predikcióit.
        """
        results = {}

        for match in matches:
            sim = self.run_simulation(match)
            prob = sim.get("win_probability", 0.5)
            odds = sim.get("odds", 2.0)

            results[match] = {
                "match": match,
                "tip": "HOME" if prob > 0.5 else "AWAY",
                "odds": odds,
                "probability": prob,
                "source": "Tippmester"
            }

        return results
