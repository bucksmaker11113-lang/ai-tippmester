# ============================================================================
#   Live Tip Engine – Tippmester Quantum Engine
#   Élő tipp generálása 14:00 után
#   Gameflow + MonteCarlo V3 + RL piaci adaptáció
# ============================================================================

import datetime


class LiveTipEngine:

    def __init__(self):
        self.live_start_hour = 14  # magyar idő szerint 14:00 után lehet live tipp

    # ----------------------------------------------------------------------
    # Időellenőrzés (14:00 után)
    # ----------------------------------------------------------------------
    def can_generate_live_tip(self):
        now = datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # CET
        return now.hour >= self.live_start_hour

    # ----------------------------------------------------------------------
    # Élő tipp generálás
    # ----------------------------------------------------------------------
    def generate(self, evaluated_live_events=None, gameflow_engine=None, rl_engine=None):

        if not self.can_generate_live_tip():
            return {
                "live_tip_available": False,
                "reason": "Live tip only available after 14:00 CET."
            }

        if evaluated_live_events is None or len(evaluated_live_events) == 0:
            return {
                "live_tip_available": False,
                "reason": "No live events available."
            }

        # gameflow alapján rendezés (támadási intenzitás)
        scored = []
        for ev in evaluated_live_events:

            gf_score = 0.0
            rl_adj = 0.0

            # gameflow engine pontszám
            if gameflow_engine:
                gf_score = gameflow_engine.predict(ev["event"])

            # reinforcement learning piaci adaptáció
            if rl_engine:
                rl_adj = rl_engine.adapt(ev["event"])

            total_score = (
                ev["strength"] * 0.3 +
                gf_score * 0.5 +
                rl_adj * 0.2
            )

            scored.append((total_score, ev))

        # a legjobb egyetlen élő tipp kiválasztása
        scored.sort(key=lambda x: x[0], reverse=True)
        best = scored[0][1]

        # jelölés
        best["event"]["tip_type"] = "live"

        return {
            "live_tip_available": True,
            "live_tip": best
        }
