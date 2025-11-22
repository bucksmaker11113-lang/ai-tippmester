from backend.core.montecarlo_engine import MonteCarloEngine
from backend.vision.vision_processor import VisionAnalyzer
from backend.fusion.mining_bridge import DataMiningBridge
import numpy as np
from datetime import datetime
import pandas as pd


class FusionController:
    """
    Fúziós AI motor – egyesíti:
    - Vision Analyzer (kép beolvasás)
    - Monte Carlo Engine (számítás)
    - Data Mining Bridge (külső visszatanuló elemzés)
    """

    def __init__(self, log_path="backend/data/fusion_log.csv"):
        self.vision = VisionAnalyzer()
        self.mc = MonteCarloEngine()
        self.bridge = DataMiningBridge()
        self.log_path = log_path

    def process_image_and_analyze(self, file_bytes: bytes):
        # 1️⃣ Kép feldolgozása (Vision Analyzer)
        vision_result = self.vision.analyze_image(file_bytes)
        match = vision_result.get("match")
        odds_list = vision_result.get("odds", [])

        if not odds_list:
            return {
                "match": match,
                "message": "Nem sikerült oddsokat kinyerni a képből.",
                "recommendation": None
            }

        # 2️⃣ Monte Carlo szimuláció Tippmester oldalon
        probs = [min(1.0, max(0.1, np.random.normal(0.55, 0.1))) for _ in odds_list]
        mc_result = self.mc.recommend(odds_list, probs)
        best_local = mc_result["best_pick"]

        # 3️⃣ Küldés a Data Mining motor felé
        mining_response = self.bridge.send_odds_data(match, odds_list)
        external_advice = None
        if match:
            external_advice = self.bridge.get_advice(match)

        # 4️⃣ Fúzió – Tippmester és Data Mining eredmények kombinálása
        recommendation = self._combine_results(match, best_local, external_advice)

        # 5️⃣ Log mentés
        self._log_fusion(match, recommendation)
        return recommendation

    def _combine_results(self, match, local, external):
        if external and "score" in external:
            combined_ev = (local["expected_value"] + external["score"]) / 2
            comment = f"{match}: Monte Carlo {local['expected_value']} · Data Mining {external['score']} → átlag: {round(combined_ev,2)}"
        else:
            combined_ev = local["expected_value"]
            comment = f"{match}: nincs külső elemzés, Monte Carlo szerint value = {combined_ev:.2f}"

        # Értelmezett AI komment
        if combined_ev > 60:
            msg = "💚 Erős value jelzés — mindkét AI szerint jó tipp!"
        elif combined_ev > 30:
            msg = "📈 Mérsékelt value – Tippmester javasolja figyelésre."
        else:
            msg = "⚠️ Gyenge jel – inkább ne kockáztass ma."

        return {
            "match": match,
            "odds": local["odds"],
            "prob": local["prob"],
            "expected_value": combined_ev,
            "comment": msg,
            "detail": comment
        }

    def _log_fusion(self, match, recommendation):
        df = pd.DataFrame([{
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "match": match,
            "odds": recommendation["odds"],
            "prob": recommendation["prob"],
            "expected_value": recommendation["expected_value"],
            "comment": recommendation["comment"]
        }])
        try:
            df.to_csv(self.log_path, mode="a", header=False, index=False)
        except Exception:
            pass
