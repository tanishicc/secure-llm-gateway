from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Client auth (comma-separated)
    api_keys: str = "dev-key-1"

    # Provider config (kept even if mock mode is enabled)
    openai_api_key: str = ""
    openai_base_url: str = "https://api.openai.com/v1"
    model_name: str = "gpt-4o-mini"

    # ✅ Mock mode (no APIs)
    mock_mode: bool = True

    # Policy thresholds
    block_threshold: int = 70

    # Rate limiting
    max_requests_per_minute: int = 30

    # Logging
    log_level: str = "INFO"

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)
    
    policy_mode: str = "standard"

settings = Settings()
