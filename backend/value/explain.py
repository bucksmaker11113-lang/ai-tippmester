"""
Explainable AI – Tippmester AI Fusion 1.0
Magyarázza a Tippmester AI döntéseit emberi nyelven.
"""

import random

class ExplainableAI:
    def __init__(self):
        self.templates = [
            "Ezt a tippet azért választottam, mert az odds {odds} és a value {value_score}.",
            "A statisztika szerint ez value-helyzet: {value_score}, ami fölötte van a küszöbnek.",
            "Ez egy kockázatosabb, de várhatóan nyereséges pozíció az odds {odds} alapján."
        ]

    def explain(self, pick, odds, value_score):
        template = random.choice(self.templates)
        return template.format(pick=pick, odds=odds, value_score=value_score)

