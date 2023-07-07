from pydantic import BaseModel
from auth.domain.entities import EmailPw

class Token(BaseModel):
    token: str

__all__ = [
    "EmailPw",
    "Token",
]
