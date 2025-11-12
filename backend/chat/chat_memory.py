"""
Chat Memory – Tippmester 5.2
Egyszerű memória az előző üzenetekhez (kontextus tanulás).
"""

import json
from datetime import datetime

class ChatMemory:
    def __init__(self, filepath="backend/data/conversation_history.db"):
        self.filepath = filepath
        self.messages = []

    def add_message(self, role, content):
        self.messages.append({"role": role, "content": content, "time": datetime.now().isoformat()})
        self._save()

    def get_recent_context(self, n=5):
        return self.messages[-n:]

    def _save(self):
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(self.messages, f, indent=2, ensure_ascii=False)
