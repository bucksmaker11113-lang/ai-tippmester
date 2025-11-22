# backend/core/fusion_engine.py

class FusionEngine:
    """
    Összefésüli a Tippmester és a Data Mining AI javaslatait.
    Ha ugyanazt a tippet adják → az bekerül.
    Ha eltérnek → súlyozott döntéssel választ.
    """

    def merge_predictions(self, tips_self, tips_dm, tips_ml, tips_bayesian):
        """
        Két forrás eredményeit egyesíti.
        Ha ugyanazt a mérkőzést javasolják → bekerül automatikusan.
        Ha eltérnek → súlyozott döntéssel választ.
        """
        merged = []
        all_matches = set(tips_self.keys()) | set(tips_dm.keys())

        for match in all_matches:
            t1 = tips_self.get(match)
            t2 = tips_dm.get(match)

            # Bayesian frissítés figyelembe vétele
            bayesian_prob = tips_bayesian.get(match, {}).get("probability", 0.5)

            if t1 and t2:
                merged.append(self._combine(t1, t2, bayesian_prob, force=True))
            elif t1:
                merged.append(self._combine(t1, bayesian_prob=bayesian_prob))
            elif t2:
                merged.append(self._combine(t2, bayesian_prob=bayesian_prob))

        return merged

    def _combine(self, t1, t2=None, bayesian_prob=0.5, force=False):
        """Két tipp kombinálása, figyelembe véve a Bayesian frissítést"""
        if t2 and force:
            avg_prob = (t1["probability"] + t2["probability"] + bayesian_prob) / 3
            return {
                "match": t1["match"],
                "tip": t1["tip"],
                "odds": max(t1["odds"], t2["odds"]),
                "probability": avg_prob,
                "source": "Fusion"
            }
        else:
            t = t1 or t2
            return {**t, "source": t.get("source", "Single")}
