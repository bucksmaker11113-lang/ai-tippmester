"""
Sentiment Collector – Tippmester AI Fusion 1.0
Piaci hangulat elemző modul.
"""

import random

class SentimentCollector:
    def __init__(self):
        pass

    def get_sentiment_index(self, match):
        """0–1 közötti érték: 0 = pesszimista piac, 1 = túl optimista piac"""
        return round(random.uniform(0.2, 0.8), 2)

