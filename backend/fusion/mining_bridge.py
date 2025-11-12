import requests
import json
import pandas as pd
from datetime import datetime

class DataMiningBridge:
    """
    Tippmester – DataMining 2.0 kapcsolat.
    Ez a modul biztosítja a kétirányú adatkapcsolatot:
    1️⃣ Tippmester -> Data Mining: odds, tippek, eredmények feltöltése
    2️⃣ Data Mining -> Tippmester: visszatanulási és prediktív elemzések lekérése
    """

    def __init__(self,
                 mining_api_base="https://data-mining-ai.onrender.com/api",
                 log_path="backend/data/mining_bridge_log.csv"):
        self.api_base = mining_api_base
        self.log_path = log_path

    # 1️⃣ Adatok küldése a Data Mining motor felé
    def send_odds_data(self, match, odds, league="unknown"):
        try:
            payload = {
                "match": match,
                "odds": odds,
                "league": league,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            response = requests.post(f"{self.api_base}/feed/odds_log", json=payload, timeout=10)
            self._log_action("SEND_ODDS", payload, response.status_code)
            return response.json() if response.status_code == 200 else None
        except Exception as e:
            self._log_error("SEND_ODDS", str(e))
            return None

    # 2️⃣ Data Mining válasz lekérése (prediktív értékelés)
    def get_advice(self, match):
        try:
            response = requests.get(f"{self.api_base}/fusion/advice", params={"match": match}, timeout=10)
            if response.status_code == 200:
                data = response.json()
                self._log_action("GET_ADVICE", {"match": match}, 200)
                return data
            else:
                self._log_action("GET_ADVICE", {"match": match}, response.status_code)
                return None
        except Exception as e:
            self._log_error("GET_ADVICE", str(e))
            return None

    # 3️⃣ Összesített elemzések lekérése (napi/havi statisztika)
    def get_global_insights(self):
        try:
            response = requests.get(f"{self.api_base}/fusion/insights", timeout=10)
            if response.status_code == 200:
                data = response.json()
                self._log_action("GET_INSIGHTS", {}, 200)
                return data
            else:
                self._log_action("GET_INSIGHTS", {}, response.status_code)
                return None
        except Exception as e:
            self._log_error("GET_INSIGHTS", str(e))
            return None

    # 4️⃣ Lokális naplózás
    def _log_action(self, action, payload, status):
        df = pd.DataFrame([{
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "action": action,
            "status": status,
            "payload": json.dumps(payload)
        }])
        df.to_csv(self.log_path, mode="a", header=False, index=False)

    def _log_error(self, action, error):
        df = pd.DataFrame([{
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "action": f"ERROR_{action}",
            "status": "FAILED",
            "payload": error
        }])
        df.to_csv(self.log_path, mode="a", header=False, index=False)
