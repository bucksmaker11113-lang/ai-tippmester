"""
Odds Aggregator – Tippmester AI Fusion 1.0
Összegyűjti a TippmixPro és nemzetközi API oddsokat.
"""

import random
import requests

class OddsAggregator:
    def __init__(self):
        self.sources = {
            "tippmixpro": "https://www.tippmixpro.hu/api/odds",
            "api_football": "https://api-football-v1.p.rapidapi.com",
        }

    def collect_odds(self, match):
        odds_data = {}
        for source, url in self.sources.items():
            try:
                # valódi API hívás helyett mock adat
                odds_data[source] = {
                    "1": round(random.uniform(1.5, 3.0), 2),
                    "X": round(random.uniform(2.5, 4.5), 2),
                    "2": round(random.uniform(1.5, 3.0), 2)
                }
            except Exception:
                continue
        return self._merge_odds(odds_data)

    def _merge_odds(self, data):
        merged = {"1": 0, "X": 0, "2": 0}
        count = len(data)
        for src in data.values():
            for k, v in src.items():
                merged[k] += v
        return {k: round(v / count, 2) for k, v in merged.items()}

