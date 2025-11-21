# ============================================================================
#   TIPPMIXPRO MATCH FINDER ENGINE – Quantum Engine 7.0
# ----------------------------------------------------------------------------
#   Feladata:
#     - Nemzetközi value tippek egyeztetése a TippmixPro kínálattal
#     - Ha nincs → automatikus helyettesítés
#     - Ha van → TippmixPro oddst ad vissza
#
# ============================================================================

class TippmixProEngine:

    def __init__(self, tippmix_data=None):
        self.tippmix_data = tippmix_data or []

    def set_data(self, data):
        self.tippmix_data = data

    def find_match(self, event):
        """
        Megkeresi van-e a TippmixPro kínálatban:
          - csapatnév alapján
          - esemény típusa (1X2, over/under stb.)
        """

        name = event["match"].lower()

        for tm in self.tippmix_data:
            if name in tm["match"].lower():
                return {
                    "found": True,
                    "odds": tm["odds"],
                    "market": tm.get("market")
                }

        return {"found": False, "odds": None}
        

tippmix_engine = TippmixProEngine()
