import requests
import random
import time
from bs4 import BeautifulSoup

# ------------------------------------------------------------
# USER AGENT GENERÁTOR – anti-bot védelem
# ------------------------------------------------------------

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (X11; Linux x86_64)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64)",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2)",
    "Mozilla/5.0 (Linux; Android 10)"
]

def get_headers():
    return {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept-Language": "en-US,en;q=0.9"
    }


# ------------------------------------------------------------
# FAIR ODDS KALKULÁTOR – több bookmaker értékéből
# ------------------------------------------------------------

def calculate_fair_odds(bookmaker_odds):
    """
    bookmaker_odds: pl. [2.10, 2.05, 2.08, 2.12]
    fair_odds = median vagy átlag
    """

    if not bookmaker_odds:
        return None

    bookmaker_odds = [o for o in bookmaker_odds if o is not None and o > 1.01]

    if len(bookmaker_odds) == 0:
        return None

    bookmaker_odds.sort()
    mid = len(bookmaker_odds) // 2

    if len(bookmaker_odds) % 2 == 1:
        return round(bookmaker_odds[mid], 2)
    else:
        return round((bookmaker_odds[mid - 1] + bookmaker_odds[mid]) / 2, 2)


# ------------------------------------------------------------
# SCRAPER MAG – sportáganként
# ------------------------------------------------------------

def scrape_oddsportal_sport(url, sport_type):
    """
    Általános OddsPortal scraping funkció.
    Sportág: soccer, basketball, hockey, tennis
    """

    try:
        html = requests.get(url, headers=get_headers(), timeout=10).text
    except:
        return []

    soup = BeautifulSoup(html, "html.parser")

    events = []

    rows = soup.select("div.eventRow")  # OddsPortal esemény sorok

    for row in rows:
        try:
            t1 = row.select_one(".participant-home").get_text(strip=True)
            t2 = row.select_one(".participant-away").get_text(strip=True)

            # oddsok kinyerése
            bookmaker_cells = row.select("div.kx")
            odds_values = []

            for cell in bookmaker_cells:
                txt = cell.get_text(strip=True)
                try:
                    val = float(txt.replace(",", "."))
                    if val > 1.01:
                        odds_values.append(val)
                except:
                    pass

            if len(odds_values) == 0:
                continue

            fair = calculate_fair_odds(odds_values)

            events.append({
                "sport": sport_type,
                "team1": t1,
                "team2": t2,
                "international_odds": max(odds_values),
                "fair_odds": fair,
                "confidence": 0.50,      # később ML-ből jön
                "prev_line": fair,
                "current_line": fair
            })

        except:
            continue

    return events


# ------------------------------------------------------------
# SPORTÁGAK URL-LISTÁJA
# ------------------------------------------------------------

URLS = {
    "foci": "https://www.oddsportal.com/matches/soccer/",
    "kosar": "https://www.oddsportal.com/matches/basketball/",
    "hoki": "https://www.oddsportal.com/matches/hockey/",
    "tenisz": "https://www.oddsportal.com/matches/tennis/"
}


# ------------------------------------------------------------
# FŐ FUNKCIÓ — komplett aggregator 4 sportágra
# ------------------------------------------------------------

def scrape_international_all():
    all_events = []

    for sport, url in URLS.items():
        time.sleep(random.uniform(0.8, 1.6))  # anti-bot delay
        data = scrape_oddsportal_sport(url, sport)
        all_events.extend(data)

    return all_events
