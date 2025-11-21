import asyncio
from playwright.async_api import async_playwright
import random

BOOKMAKER_URLS = {
    "pinnacle": "https://www.pinnacle.com/en/soccer/matchups",
    "bet365": "https://www.bet365.com/#/AC/B1/",
    "unibet": "https://www.unibet.com/betting/sports/filter/all/all/all/matches",
    "tippmixpro": "https://www.tippmixpro.hu/sportfogadas"
}

async def scrape_playwright():
    events = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        for name, url in BOOKMAKER_URLS.items():
            try:
                await page.goto(url, timeout=15000)
                await page.wait_for_timeout(2000)

                html = await page.content()

                # A továbbiakban HTML → match parser
                # (A custom parser később beépítésre kerül sportáganként)

                events.append({
                    "source": name,
                    "html": html[:5000]  # debug
                })
            except:
                continue

        await browser.close()
    return events


def collect_events():
    # FUTTATJA az async Playwright-ot sync környezetben
    loops = asyncio.new_event_loop()
    asyncio.set_event_loop(loops)
    html_data = loops.run_until_complete(scrape_playwright())

    # DEMO GENERÁTOR — az AI működéséhez
    events = []

    for e in html_data:
        events.append({
            "match": "Team A - Team B",
            "sport": "football",
            "prematch": {"fair_odds": random.uniform(1.5, 3.0)},
            "live": {},
            "odds": {"prev_odds": random.uniform(1.5, 3.0), "current_odds": random.uniform(1.5, 3.0)},
            "bookmakers": {
                "pin_prev": random.uniform(1.5, 3.0),
                "pin_cur": random.uniform(1.5, 3.0),
                "pin_volume": random.uniform(1000, 3000),
                "b365_prev": random.uniform(1.5, 3.0),
                "b365_cur": random.uniform(1.5, 3.0),
                "public_money": random.uniform(20, 80),
                "uni_prev": random.uniform(1.5, 3.0),
                "uni_cur": random.uniform(1.5, 3.0),
                "uni_volume": random.uniform(200, 900),
                "tpro_prev": random.uniform(1.5, 3.0),
                "tpro_cur": random.uniform(1.5, 3.0),
                "tpro_lag": random.uniform(1, 60)
            },
            "tm_odds": random.uniform(1.5, 3.0),
            "reasoning": {
                "derby": False,
                "importance": random.randint(1, 10),
                "minute": random.randint(1, 90),
                "tempo": random.randint(3, 8),
                "danger": random.randint(10, 80),
                "emotion": random.randint(1, 10),
                "variance": random.uniform(0.05, 0.25),
                "home_adv": random.randint(1, 10),
                "rain": False,
                "wind": random.uniform(0, 40)
            }
        })

    return events
