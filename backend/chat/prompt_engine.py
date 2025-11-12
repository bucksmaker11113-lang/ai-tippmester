"""
Prompt Engine – Tippmester 5.2
Humoros, véletlenszerű magyar válaszok generálása Mesterkéhez.
"""

import random
import json

class PromptEngine:
    def __init__(self, humor_file="backend/reports/humor_quotes.json"):
        try:
            with open(humor_file, "r", encoding="utf-8") as f:
                self.humor_data = json.load(f)
        except Exception:
            self.humor_data = {
                "vicces": ["Na, ez az odds még a nagymamámnak is tetszene!", "Az esély kicsi, de a remény örök."],
                "komoly": ["A statisztika most nem kedvez ennek a tippnek.", "Ezt inkább hagyjuk, nincs benne value."],
                "sportos": ["Ez a meccs igazi derbi lesz, tartsd a bankrollt stabilan."],
                "nyugodt": ["Semmi rohanás, a jó tipp mindig jön magától."]
            }

    def generate_response(self, message, humor_level="vicces"):
        options = self.humor_data.get(humor_level, [])
        if not options:
            return "Nem tudom, mit mondjak, de biztos, hogy Mesterke figyel!"
        return random.choice(options)
