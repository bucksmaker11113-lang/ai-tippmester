# ============================================================================
#   Kombi Tip Engine – Tippmester Quantum Engine
#   4–5 tippből álló kombi ajánlás generálása
#   Szabályok:
#       - nem használhat single tippekből származó meccseket
#       - value alapján rendez
#       - odds ~2.00 körül
#       - 4–5 esemény
# ============================================================================

class KombiTipEngine:

    def __init__(self):
        self.min_tips = 4
        self.max_tips = 5
        self.min_odds = 1.60
        self.max_odds = 3.00

    # ----------------------------------------------------------------------
    # Kombi generálás
    # ----------------------------------------------------------------------
    def generate(self, evaluated_events=None, single_tips=None):

        if evaluated_events is None:
            return []

        # single meccsek kizárása
        single_ids = set()

        if single_tips:
            for s in single_tips:
                ev = s["event"]
                match_id = ev.get("match_id")
                if match_id:
                    single_ids.add(match_id)

        # szűrés azokból, amik NEM single-ek voltak
        candidates = []
        for ev in evaluated_events:
            match_id = ev["event"].get("match_id")
            if match_id not in single_ids:
                candidates.append(ev)

        # odds tartományra szűrés
        candidates = [
            ev for ev in candidates
            if self.min_odds <= ev["event"].get("odds", 2.0) <= self.max_odds
        ]

        # value szerint rendezés
        candidates.sort(key=lambda x: x["value"], reverse=True)

        # kiválasztás
        kombi = candidates[:self.max_tips]

        # ha túl kevés, nincs kombi tipp
        if len(kombi) < self.min_tips:
            return []

        # jelölés
        for item in kombi:
            item["event"]["tip_type"] = "kombi"

        return kombi
