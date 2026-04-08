from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_env: str = "development"
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    database_url: str = "sqlite+aiosqlite:///./hutch_notify.db"
    api_key: str = "change-me"

    apns_key_id: str
    apns_team_id: str
    apns_bundle_id: str
    apns_private_key_path: str

    srht_token: str
    poll_interval_seconds: int = 120
    log_level: str = "INFO"


settings = Settings()
