from pydantic import BaseModel


class SecretSanta(BaseModel):
    secretSanta: any
