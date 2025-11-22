"""
Config Loader – Tippmester AI Fusion 1.0
.env és config beállítások betöltése Railway és lokális környezetben.
"""

import os
from dotenv import load_dotenv


class Config:
    def __init__(self, env_path: str = ".env"):
        # .env betöltése, ha létezik
        if os.path.exists(env_path):
            load_dotenv(env_path)

        # ---- Email beállítások ----
        self.email_sender = os.getenv("EMAIL_SENDER", "")
        self.email_password = os.getenv("EMAIL_PASSWORD", "")
        self.email_host = os.getenv("EMAIL_HOST", "smtp.gmail.com")
        self.email_port = int(os.getenv("EMAIL_PORT", 587))

        # ---- AI kapcsolatok ----
        self.data_mining_url = os.getenv("DATA_MINING_URL", "http://localhost:9000")
        self.api_key = os.getenv("API_KEY", "")
        self.debug = os.getenv("DEBUG", "True") == "True"

        # ---- App beállítások ----
        self.port = int(os.getenv("PORT", 8000))
        self.vision_enabled = os.getenv("VISION_ENABLED", "True") == "True"
        self.humor_mode = os.getenv("HUMOR_MODE", "True") == "True"

        # ---- Logolás / üzemmód ----
        self.env = os.getenv("ENVIRONMENT", "development")
        self.log_level = os.getenv("LOG_LEVEL", "INFO")

    def summary(self):
        """Debug segéd: kiírja az aktuális konfig állapotot."""
        return {
            "email_sender": self.email_sender,
            "data_mining_url": self.data_mining_url,
            "port": self.port,
            "debug": self.debug,
            "env": self.env
        }


# Példa használat
if __name__ == "__main__":
    cfg = Config()
    print(cfg.summary())
