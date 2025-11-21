# ==========================================================
#  HUMAN-LIKE REASONING LAYER – Quantum Engine 7.0
# ==========================================================
#
#  Olyan logika, amit profi sportfogadók alkalmaznak:
#   - derbi faktor
#   - motiváció
#   - fáradás
#   - meccs tempója
#   - veszélyzónák (danger zone)
#   - variance szint
#   - időjárás hatás (ha van adat)
#   - tét fontossága
#   - hazai pálya faktor
#
#  Kimenet: reasoning_score (0–1)
# ==========================================================

import math


class ReasoningLayer:

    def __init__(self):
        pass

    # ------------------------------------------------------
    # Derbi faktor (rivalizálás)
    # ------------------------------------------------------
    def derby_factor(self, derby=False):
        if derby:
            return 0.15     # magas intenzitás, extra gól esély
        return 0.0

    # ------------------------------------------------------
    # Motiváció – fontos meccs?
    # ------------------------------------------------------
    def motivation_factor(self, importance_level):
        """
        importance_level = 0–10
        """
        return min(0.2, importance_level * 0.02)

    # ------------------------------------------------------
    # Fáradás – perc + tempó alapján
    # ------------------------------------------------------
    def fatigue_factor(self, minute, tempo_score):
        fatigue = (minute / 90.0) * (tempo_score / 10.0)
        return min(0.20, fatigue)

    # ------------------------------------------------------
    # Danger Zone – veszélyes támadások
    # ------------------------------------------------------
    def danger_zone_factor(self, da):
        if da > 60:
            return 0.25
        elif da > 40:
            return 0.15
        elif da > 25:
            return 0.05
        return 0.0

    # ------------------------------------------------------
    # Emotional Probability – szurkolói nyomás
    # ------------------------------------------------------
    def emotional_factor(self, home_pressure):
        return min(0.1, home_pressure * 0.01)

    # ------------------------------------------------------
    # Variance szint – mennyire kiszámítható a meccs?
    # ------------------------------------------------------
    def variance_penalty(self, variance_level):
        if variance_level > 0.25:
            return -0.15
        elif variance_level > 0.15:
            return -0.08
        return 0.0

    # ------------------------------------------------------
    # Hazai pálya faktor
    # ------------------------------------------------------
    def home_advantage(self, home_adv):
        return min(0.10, home_adv * 0.01)

    # ------------------------------------------------------
    # Weather (ha van adat)
    # ------------------------------------------------------
    def weather_factor(self, rain=False, wind_speed=0):
        rf = -0.05 if rain else 0.0
        ws = -min(0.05, wind_speed / 100)
        return rf + ws

    # ------------------------------------------------------
    # Master reasoning score
    # ------------------------------------------------------
    def reasoning_score(self, ctx):
        """
        ctx:
        {
          "derby": bool,
          "importance": 0-10,
          "minute": int,
          "tempo": 0-10,
          "danger": int,
          "emotion": 0-10,
          "variance": float,
          "home_adv": 0-10,
          "rain": bool,
          "wind": float
        }
        """

        s = 0

        s += self.derby_factor(ctx.get("derby", False))
        s += self.motivation_factor(ctx.get("importance", 5))
        s += self.fatigue_factor(ctx.get("minute", 45), ctx.get("tempo", 5))
        s += self.danger_zone_factor(ctx.get("danger", 20))
        s += self.emotional_factor(ctx.get("emotion", 5))
        s += self.home_advantage(ctx.get("home_adv", 5))
        s += self.weather_factor(ctx.get("rain", False), ctx.get("wind", 0))

        s += self.variance_penalty(ctx.get("variance", 0.1))

        # Normalizáció
        s = max(0.0, min(1.0, (s + 0.2)))

        return s


# GLOBAL INSTANCE
reasoning_engine = ReasoningLayer()
