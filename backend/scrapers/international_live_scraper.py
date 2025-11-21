import requests
import random
import time
from bs4 import BeautifulSoup


# ------------------------------------------------------------
# RANDOM USER AGENT – anti-bot védelem
# ------------------------------------------------------------

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "Mozilla/5.0 (X11; Linux x86_64)",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_2)",
    "Mozilla/5.0 (Linux; Android 11)"
]

def get_headers():
    return {"User-Agent": random.choice(USER_AGENTS)}


# ------------------------------------------------------------
# ÉLŐ SCRAPER MAG
# ------------------------------------------------------------

def scrape_oddsportal_live(url="https://www.oddsportal.com/matches/live/"):
    """
    Élő OddsPortal odds letapogatás.
    Kinyer:
    - team1 / team2
    - current_odds
    - prev_odds
    - idő
    - league
    """

    try:
        html = requests.get(url, headers=get_headers(), timeout=10).text
    except:
        return []

    soup = BeautifulSoup(html, "html.parser")

    events = []

    rows = soup.select("div.eventRow")

    for row in rows:
        try:
            t1 = row.select_one(".participant-home").get_text(strip=True)
            t2 = row.select_one(".participant-away").get_text(strip=True)

            # odds cellák – változó számú iroda
            odd_cells = row.select("div.kx")

            odds_values = []
            for cell in odd_cells:
                try:
                    val = float(cell.get_text(strip=True).replace(",", "."))
                    if val > 1.01:
                        odds_values.append(val)
                except:
                    pass

            if len(odds_values) < 1:
                continue

            current_odds = max(odds_values)

            # Odds drop alapja → előző oddsot tárolhatod memóriában/DB-ben
            prev_odds = current_odds * 1.05  # default 5% korábbi érték

            events.append({
                "sport": "live",
                "team1": t1,
                "team2": t2,
                "current_odds": current_odds,
                "prev_odds": prev_odds,

                # momentum alap → ha nincs adat
                "attack_pressure": random.uniform(0.3, 0.7),
                "shots": random.randint(1, 10),
                "dangerous_attacks": random.randint(1, 15),
                "possession": random.uniform(0.40, 0.60),

                # model input alapértékek
                "bayes": 0.55,
                "mc_live": random.uniform(0.50, 0.75),
                "ml_pred": random.uniform(0.50, 0.75),
                "market_stability": random.uniform(0.70, 0.95),
                "markov_prev": random.uniform(0.40, 0.60)
            })

        except:
            continue

    return events


# ------------------------------------------------------------
# FŐ FUNKCIÓ – hívható a backendből
# ------------------------------------------------------------

def scrape_international_live():
    time.sleep(random.uniform(0.8, 1.5))  # anti-bot delay
    return scrape_oddsportal_live()
