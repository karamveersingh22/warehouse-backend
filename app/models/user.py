from pydantic import BaseModel
from typing import Optional


class UserInDB(BaseModel):
    username: str
    password_hash: str
    role: str  # "manager" or "worker"
