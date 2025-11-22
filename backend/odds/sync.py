"""
Odds Sync – Tippmester AI Fusion 1.0
Szinkronizálja a TippmixPro oddsokat a nemzetközi piacokkal.
"""

from .aggregator import OddsAggregator

class OddsSync:
    def __init__(self):
        self.aggregator = OddsAggregator()

    def sync_odds(self, match):
        merged_odds = self.aggregator.collect_odds(match)
        return merged_odds

