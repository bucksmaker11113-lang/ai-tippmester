# ============================================================================
#   Single Tip Engine – Tippmester Quantum Engine
#   Napi 4 single tipp generálása:
#       - 1 foci
#       - 1 kosár
#       - 1 jégkorong
#       - 1 tenisz
# ============================================================================

class SingleTipEngine:

    def __init__(self):
        # a sportágak, fix 4 single tipp
        self.target_sports = ["football", "basketball", "hockey", "tennis"]

    # ----------------------------------------------------------------------
    # Napi single tippek generálása
    # ----------------------------------------------------------------------
    def generate(self, evaluated_events=None):
        """
        evaluated_events = QuantumSynthEngine.synthesize() eredménye
        Minden event-ben van:
            - sport
            - value
            - fair_odds
            - stake
            - tippmix_odds (ha elérhető)
        """

        if evaluated_events is None:
            return []

        single_tips = []

        for sport in self.target_sports:

            # sportágszűrés
            sport_events = [
                ev for ev in evaluated_events
                if ev["event"].get("sport", "").lower() == sport
            ]

            if not sport_events:
                continue

            # a legjobb value alapján választunk
            best = sorted(sport_events, key=lambda x: x["value"], reverse=True)[0]

            # jelölés
            best["event"]["tip_type"] = "single"

            single_tips.append(best)

        return single_tips
