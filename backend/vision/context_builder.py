"""
Vision Context Builder – Tippmester AI Fusion 1.0
Szöveg értelmezése OCR után.
"""

import re

class VisionContextBuilder:
    def extract_context(self, text: str):
        """Kinyeri a csapatneveket és oddsokat a nyers szövegből."""
        lines = [line.strip() for line in text.split("\n") if line.strip()]
        context = {"teams": [], "odds": {}}
        for line in lines:
            if re.search(r"\d+\.\d+", line):
                odds = re.findall(r"\d+\.\d+", line)
                if len(odds) == 3:
                    context["odds"] = {"1": float(odds[0]), "X": float(odds[1]), "2": float(odds[2])}
            elif "-" in line or "vs" in line.lower():
                parts = re.split(r"[-vVsS]+", line)
                if len(parts) >= 2:
                    context["teams"] = [p.strip() for p in parts[:2]]
        return context

