"""
Vision Validator – Tippmester AI Fusion 1.0
A felismerett eseményeket validálja a Fusion Connectorral.
"""

from backend.core.fusion_connector import FusionConnector

class VisionValidator:
    def __init__(self, api_key=None):
        self.fusion = FusionConnector(api_key)

    def validate(self, context):
        teams = context.get("teams", [])
        odds = context.get("odds", {})
        if not teams or not odds:
            return {"status": "error", "detail": "Hiányos adat a képen"}
        match_name = f"{teams[0]} vs {teams[1]}"
        pick = "1"  # egyszerűsített választás
        return self.fusion.validate_tip(match_name, pick, odds)

