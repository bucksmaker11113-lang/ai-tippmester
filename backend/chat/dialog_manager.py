"""
Tippmester AI Fusion 1.0 – Dialog Manager
Kétirányú chat kezelése: felhasználó ↔ Mesterke.
"""

import random
import json
from datetime import datetime
from .prompt_engine import PromptEngine
from .chat_memory import ChatMemory
from .feedback_learner import FeedbackLearner

class DialogManager:
    def __init__(self):
        self.prompter = PromptEngine()
        self.memory = ChatMemory()
        self.feedback = FeedbackLearner()

    def respond(self, user_message: str):
        """Mesterke válaszol a felhasználó üzenetére."""
        context = self.memory.get_recent_context()
        humor_level = random.choice(["vicces", "komoly", "sportos", "nyugodt"])
        response = self.prompter.generate_response(user_message, humor_level)

        self.memory.add_message("user", user_message)
        self.memory.add_message("mesterke", response)
        self.feedback.track_interaction(user_message, response)
        return {
            "timestamp": datetime.now().isoformat(),
            "response": response,
            "humor_level": humor_level
        }

