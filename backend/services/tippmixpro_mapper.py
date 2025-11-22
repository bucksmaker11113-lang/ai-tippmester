from services.normalizer import normalize_text, alias, match_team_name

# ---------------------------------------------------------
# TIPPMIXPRO MAPPER – nemzetközi odds → TMPro event párosítás
# ---------------------------------------------------------

def map_events_to_tippmixpro(international_events, tippmixpro_events):
    """
    Párosítja a nemzetközi tippeket a TippmixPro kínálattal.
    Minden esemény normalizálva összehasonlításra kerül.
    """

    mapped = []

    for intl in international_events:
        team1_int = alias(intl.get("team1", ""))
        team2_int = alias(intl.get("team2", ""))

        for tm in tippmixpro_events:

            team1_tm = alias(tm.get("team1", ""))
            team2_tm = alias(tm.get("team2", ""))

            # kétirányú egyezés
            if match_team_name(team1_int, team1_tm) and match_team_name(team2_int, team2_tm):
                mapped.append({
                    "sport": intl.get("sport"),
                    "team1": intl.get("team1"),
                    "team2": intl.get("team2"),

                    # oddsok
                    "international_odds": intl.get("odds"),
                    "tippmix_odds": tm.get("odds"),

                    # model inputok
                    "fair_odds": intl.get("fair_odds"),
                    "confidence": intl.get("confidence"),
                    "prev_line": intl.get("prev_line"),
                    "current_line": intl.get("current_line"),

                    # tippmix referencia
                    "tippmix_event": tm
                })

    return mapped
