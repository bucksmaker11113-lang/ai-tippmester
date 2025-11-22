"""
Fusion Bridge – Tippmester AI Fusion 1.0
Kapcsolat a Tippmester és a Data Mining 2.0 API között.
"""

import requests

class FusionBridge:
    def __init__(self, api_key=None):
        self.api_key = api_key
        self.endpoint = "https://data-mining-2-0.onrender.com/api/fusion"

    def send_event(self, event_data):
        headers = {"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}
        try:
            r = requests.post(f"{self.endpoint}/event", json=event_data, headers=headers, timeout=5)
            return r.json()
        except Exception as e:
            return {"status": "error", "detail": str(e)}

