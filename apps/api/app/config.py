import os

class Settings:
    log_level: str = os.getenv("LOG_LEVEL", "info").lower()

settings = Settings()