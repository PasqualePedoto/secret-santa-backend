from pydantic import BaseModel
from typing import Any


class SecretSanta(BaseModel):
    secretSanta: Any
