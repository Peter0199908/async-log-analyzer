from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import HttpUrl

class Settings(BaseSettings):
    WEBHOOK_URL: HttpUrl
    ALERT_THRESHOLD_COUNT: int = 3
    ALERT_TIME_WINDOW_SECONDS: int = 60

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()