from pydantic import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "chat-microservice"
    GEMINI_MODEL: str = "gemini-pro-latest"

settings = Settings()
