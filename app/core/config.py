from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql://user:password@localhost:5432/volunteer_ops"
    secret_key: str = "changeme"
    access_token_expire_minutes: int = 30

    # V2 — Slack integration
    slack_bot_token: Optional[str] = None
    slack_channel_id: Optional[str] = None

    # V2 — Google Sheets integration
    google_sheets_credentials_file: Optional[str] = None
    google_sheet_id: Optional[str] = None

    # V2 — Email integration
    email_api_key: Optional[str] = None
    email_from: Optional[str] = None

    # V3 — Operations Copilot LLM
    anthropic_api_key: Optional[str] = None

    class Config:
        env_file = ".env"


settings = Settings()
