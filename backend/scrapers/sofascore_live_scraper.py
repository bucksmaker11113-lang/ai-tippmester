import requests
import random
import time

BASE = "https://api.sofascore.com/api/v1"


# -----------------------------------------------------------
# USER-AGENT RANDOMIZÁCIÓ (SofaScore anti-bot ellen)
# -----------------------------------------------------------
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "Mozilla/5.0 (X11; Linux x86_64)",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_2)"
]

def headers():
    return {"User-Agent": random.choice(USER_AGENTS)}


# -----------------------------------------------------------
# 1) ÉLŐ MECCSEK LEKÉRÉSE SOFASCORE-TÓL
# -----------------------------------------------------------
def fetch_live_matches():
    url = f"{BASE}/sport/0/events/live"
    r = requests.get(url, headers=headers(), timeout=10)
    data = r.json()

    live_events = []
    for item in data.get("events", []):
        live_events.append({
            "id": item["id"],
            "sport_id": item["tournament"]["sport"]["id"],
            "sport_name": item["tournament"]["sport"]["name"],
            "home": item["homeTeam"]["name"],
            "away": item["awayTeam"]["name"],
        })

    return live_events


# -----------------------------------------------------------
# 2) STATOK LEKÉRÉSE SPORTÁGANKÉNT
# -----------------------------------------------------------
def fetch_stats(event_id):
    url = f"{BASE}/event/{event_id}/statistics"
    r = requests.get(url, headers=headers(), timeout=10)

    try:
        stats = r.json()
    except:
        return {}

    extracted = {
        "shots": 0,
        "shots_on_target": 0,
        "dangerous_attacks": 0,
        "possession": 0.50,
        "xg_home": 0.0,
        "xg_away": 0.0,
        "momentum": 0.50
    }

    categories = stats.get("statistics", [])

    for block in categories:
        for s in block.get("groups", []):
            name = s.get("name", "")
            val_home = s.get("home", {}).get("value", 0)
            val_away = s.get("away", {}).get("value", 0)

            # FOCI STATOK
            if name == "Shots":
                extracted["shots"] = val_home + val_away
            if name == "Shots on target":
                extracted["shots_on_target"] = val_home + val_away
            if name == "Dangerous attacks":
                extracted["dangerous_attacks"] = val_home + val_away
            if name == "Ball possession":
                extracted["possession"] = val_home / 100.0
            if name == "Expected goals":
                extracted["xg_home"] = float(val_home)
                extracted["xg_away"] = float(val_away)

    return extracted


# -----------------------------------------------------------
# 3) EREDMÉNY / ÓRA / IDŐ LEKÉRÉS
# -----------------------------------------------------------
def fetch_event_details(event_id):
    url = f"{BASE}/event/{event_id}"
    r = requests.get(url, headers=headers(), timeout=10)

    try:
        info = r.json()["event"]
    except:
        return {}

    return {
        "home_score": info.get("homeScore", {}).get("current"),
        "away_score": info.get("awayScore", {}).get("current"),
        "time": info.get("status", {}).get("description"),
        "clock": info.get("status", {}).get("matchTime", 0)
    }


# -----------------------------------------------------------
# 4) ODDS (ha SofaScore ad) – optional
# -----------------------------------------------------------
def fetch_event_odds(event_id):
    try:
        url = f"{BASE}/event/{event_id}/odds/1"
        r = requests.get(url, headers=headers(), timeout=10)
        data = r.json()

        markets = data.get("markets", [])
        if not markets:
            return None

        selections = markets[0].get("selections", [])
        if not selections:
            return None

        # pl. {home: 1.75, draw: 3.40, away: 4.10}
        odds = {sel["name"]: sel["odds"] for sel in selections}
        return odds

    except:
        return None


# -----------------------------------------------------------
# 5) MOMENTUM KALKULÁCIÓ (xG, shot, attempt mix)
# -----------------------------------------------------------
def calculate_momentum(stats):
    """
    Momentum modell:
    50% xG trend
    30% shots_on_target
    20% dangerous_attacks
    """
    xg_total = stats["xg_home"] + stats["xg_away"]
    if xg_total == 0:
        xg_factor = 0.50
    else:
        xg_factor = stats["xg_home"] / xg_total

    shot_factor = min(stats["shots_on_target"] / 10, 1)
    atk_factor = min(stats["dangerous_attacks"] / 20, 1)

    momentum = (
        0.5 * xg_factor +
        0.3 * shot_factor +
        0.2 * atk_factor
    )

    return round(momentum, 4)


# -----------------------------------------------------------
# 6) FŐ FÜGGVÉNY – teljes SofaScore élő motor
# -----------------------------------------------------------
def scrape_sofascore_live():
    events = fetch_live_matches()
    final_data = []

    for e in events:
        time.sleep(0.3)  # anti-bot

        stats = fetch_stats(e["id"])
        details = fetch_event_details(e["id"])
        odds = fetch_event_odds(e["id"])

        stats["momentum"] = calculate_momentum(stats)

        final_data.append({
            "event_id": e["id"],
            "sport": e["sport_name"].lower(),
            "team1": e["home"],
            "team2": e["away"],

            # statok
            "shots": stats["shots"],
            "shots_on_target": stats["shots_on_target"],
            "dangerous_attacks": stats["dangerous_attacks"],
            "possession": stats["possession"],
            "xg_home": stats["xg_home"],
            "xg_away": stats["xg_away"],
            "momentum": stats["momentum"],

            # eredmény, idő
            "home_score": details.get("home_score"),
            "away_score": details.get("away_score"),
            "clock": details.get("clock"),
            "time_status": details.get("time"),

            # odds
            "odds": odds
        })

    return final_data
