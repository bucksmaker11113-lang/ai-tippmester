# backend/core/value_analyzer.py

from backend.core.montecarlo_engine import MonteCarloEngine
from backend.core.bayesian_updater import BayesianUpdater
from backend.core.fusion_engine import FusionEngine
from backend.services.data_mining_bridge import DataMiningBridge

class ValueAnalyzer:
    """
    Tippmester Value Analyzer – két szál:
    1️⃣ Saját Monte Carlo + ML predikciók
    2️⃣ AI Data Mining javaslatok beépítése
    """

    def __init__(self):
        self.mc_engine = MonteCarloEngine()
        self.dm_bridge = DataMiningBridge()
        self.fusion = FusionEngine()
        self.bayesian_updater = BayesianUpdater(prior_probabilities=[0.5, 0.5])  # Kezdeti 50-50 valószínűség

    def run_dual_stream(self, matches):
        """
        Fő belépési pont – két szál párhuzamos futtatása.
        1️⃣ Tippmester saját Monte Carlo szimulációk
        2️⃣ Data Mining AI tanácsok lekérése
        Ezután a FusionEngine egyesíti az eredményeket.
        """
        tips_self = self.mc_engine.find_value_odds(matches)  # Szál 1
        tips_dm = self.dm_bridge.get_advice_batch(matches)  # Szál 2
        
        # Bayesian frissítés (aktualizáljuk a valószínűségeket)
        for match in matches:
            new_data = tips_dm.get(match) or tips_self.get(match)
            updated_probabilities = self.bayesian_updater.update(new_data, likelihood=0.7)  # Például 70%-os valószínűség
            tips_self[match]["probability"] = updated_probabilities[0]  # Frissítjük a tippet

        final_tips = self.fusion.merge_predictions(tips_self, tips_dm)
        return final_tips
