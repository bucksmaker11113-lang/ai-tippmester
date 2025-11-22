# ==============================================================================
#   TIPPMIXPRO SCRAPER – Quantum Engine 7.5 ULTRA
# ------------------------------------------------------------------------------
#   Feladata:
#     - tippmixpro.hu teljes sportkínálatának lekérése
#     - események neve
#     - piac típus
#     - odds
#     - sportág felismerés
# ==============================================================================

import asyncio
from playwright.async_api import async_playwright

class TippmixScraper:

    async def scrape(self):
        print("[SCRAPER] TippmixPro betöltése...")

        result = []

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()

            await page.goto("https://www.tippmixpro.hu/jatekok/fogadas/sportfogadas")

            # megvárjuk amíg betölt mindent
            await page.wait_for_timeout(3000)

            events = await page.query_selector_all(".event-row")

            for ev in events:
                try:
                    match = await ev.query_selector(".match-name")
                    match_name = await match.inner_text() if match else None

                    odds_el = await ev.query_selector(".odd-value")
                    odds = float((await odds_el.inner_text()).replace(",", ".")) if odds_el else None

                    sport = await ev.get_attribute("data-sport")

                    result.append({
                        "match": match_name,
                        "odds": odds,
                        "sport": sport,
                        "market": "1X2"
                    })
                except:
                    continue

            await browser.close()

        print(f"[SCRAPER] {len(result)} mérkőzés beolvasva.")
        return result


tippmixpro_scraper = TippmixScraper()
