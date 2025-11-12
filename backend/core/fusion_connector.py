"""
Data Mining 2.0 kapcsolódás
Tippmester és Fusion Data Intelligence közötti adatcsatorna.
"""

import requests

class FusionConnector:
    def __init__(self, api_key=None):
        self.api_key = api_key
        self.endpoint = "https://data-mining-2-0.onrender.com/api/fusion"

    def validate_tip(self, match, pick, odds):
        """Kapcsolódik a Data Mining 2.0 motorhoz validációhoz."""
        payload = {"match": match, "pick": pick, "odds": odds}
        headers = {"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}
        try:
            r = requests.post(f"{self.endpoint}/validate", json=payload, headers=headers, timeout=5)
            return r.json()
        except Exception as e:
            return {"status": "error", "detail": str(e)}
