from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    GEMINI_CHAT_MODEL: str = "gemini-flash-latest"
    GEMINI_GENERATE_MODEL: str = "gemini-pro-latest"
    GEMINI_API_KEY: str = Field(alias="GOOGLE_GEMINI_KEY")

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
