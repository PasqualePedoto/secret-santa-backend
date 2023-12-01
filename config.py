from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    EMAIL: str
    PASSWORD: str
    SERVER_NAME: str
    SERVER_PORT: int

    class Config:
        env_file = "./.env"