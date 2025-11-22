# ============================================================================
#   MatchFinder Engine – Tippmester Quantum Engine
#   Nemzetközi value tippek összehangolása TippmixPro kínálattal.
#   Ha a value tipp NINCS a TippmixPro-n:
#       -> alternatív helyettesítő esemény keresése
# ============================================================================

class MatchFinder:

    def __init__(self):
        pass

    # ----------------------------------------------------------------------
    # Egyezés vizsgálata TippmixPro kínálattal
    # ----------------------------------------------------------------------
    def match_event(self, intl_event, tippmix_events):

        home_i = intl_event.get("team_home", "").lower()
        away_i = intl_event.get("team_away", "").lower()
        sport_i = intl_event.get("sport", "").lower()

        # elsődleges full match keresés
        for tm in tippmix_events:
            home_t = tm.get("team_home", "").lower()
            away_t = tm.get("team_away", "").lower()
            sport_t = tm.get("sport", "").lower()

            if (
                sport_i == sport_t and
                home_i in home_t and
                away_i in away_t
            ):
                # teljes egyezés
                return tm

        return None  # nem talált egyezést

    # ----------------------------------------------------------------------
    # Alternatív meccs keresése
    # ----------------------------------------------------------------------
    def find_alternative(self, intl_event, tippmix_events):

        sport_i = intl_event.get("sport", "").lower()

        # ugyanabból a sportágból hasonló oddsú esemény
        intl_odds = intl_event.get("odds", 2.00)

        candidates = []

        for tm in tippmix_events:
            if tm.get("sport", "").lower() == sport_i:
                diff = abs(tm.get("odds", 2.0) - intl_odds)
                candidates.append((diff, tm))

        if not candidates:
            return None

        # a legkisebb odds-eltérésű esemény kerül kiválasztásra
        candidates.sort(key=lambda x: x[0])
        return candidates[0][1]

    # ----------------------------------------------------------------------
    # Publikus API – összehangolt lista visszaadása
    # ----------------------------------------------------------------------
    def align(self, intl_events, tippmix_events):
        """
        intl_events: a nemzetközi value tippek listája
        tippmix_events: TippmixPro scraperből
        """

        aligned = []

        for ev in intl_events:
            match = self.match_event(ev, tippmix_events)

            if match:
                # ha van tippmix-es meccs → azt használjuk
                ev["tippmix_odds"] = match.get("odds", ev.get("odds"))
                ev["tippmix_found"] = True
                aligned.append(ev)
            else:
                # ha nincs → alternatív esemény keresése
                alt = self.find_alternative(ev, tippmix_events)

                if alt:
                    ev["tippmix_odds"] = alt.get("odds")
                    ev["tippmix_found"] = False
                    ev["alternative_event"] = alt
                    aligned.append(ev)

                # ha még alternatíva sincs → kihagyjuk
                # (ritka eset, de ilyenkor nem ajánl tippet)
                # Nem tesszük hozzá az aligned listához

        return aligned
