from pydantic_settings import BaseSettings
from typing import Any

class Settings(BaseSettings):
    EMAIL: Any
    PASSWORD: Any
    SERVER_NAME: Any
    SERVER_PORT: Any

    class Config:
        env_file = "./.env"

settings = Settings()