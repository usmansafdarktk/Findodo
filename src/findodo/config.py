from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, SecretStr

class Settings(BaseSettings):
    """
    Centralized configuration for FinDodo.
    Reads from environment variables and .env files automatically.
    """
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    # Required: Will crash immediately with a clear error if missing
    openai_api_key: SecretStr = Field(alias="OPENAI_API_KEY")

    # Defaults
    default_model: str = "gpt-4-turbo-preview"
    sec_identity: str = "FinDodo Research findodo@example.com"
    chunk_size: int = 1024
    chunk_overlap: int = 100

# Singleton instance
settings = Settings()