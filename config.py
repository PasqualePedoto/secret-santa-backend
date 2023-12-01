from pydantic import BaseSettings

class Settings(BaseSettings):
    EMAIL: str
    PASSWORD: str

    class Config:
        env_file = "./.env"