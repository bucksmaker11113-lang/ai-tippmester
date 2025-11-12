"""
Config Loader – Tippmester 5.2
.env és config beállítások betöltése.
"""

import os
from dotenv import load_dotenv

class Config:
    def __init__(self, env_path=".env"):
        load_dotenv(env_path)
        self.email = os.getenv("EMAIL_SENDER")
        self.password = os.getenv("EMAIL_PASSWORD")
        self.vision_enabled = os.getenv("VISION_ENABLED", "True") == "True"
        self.humor_mode = os.getenv("HUMOR_MODE", "True") == "True"
