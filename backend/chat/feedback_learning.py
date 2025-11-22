"""
Feedback Learner – Tippmester AI Fusion 1.0
Tanul a felhasználó viselkedéséből (pozitív / negatív visszajelzések).
"""

import json

class FeedbackLearner:
    def __init__(self, filepath="backend/data/chat_feedback.json"):
        self.path = filepath
        self.stats = {"positive": 0, "negative": 0}

    def track_interaction(self, user_message, response):
        if any(x in user_message.lower() for x in ["jó", "szuper", "köszi"]):
            self.stats["positive"] += 1
        elif any(x in user_message.lower() for x in ["rossz", "nem", "hülyeség"]):
            self.stats["negative"] += 1
        self._save()

    def _save(self):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.stats, f, indent=2, ensure_ascii=False)

