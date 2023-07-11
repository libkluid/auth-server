from pydantic import BaseModel

from auth.domain.entities import EmailPw


class Token(BaseModel):
    token: str

class ChangePassword(BaseModel):
    token: str
    password: str


__all__ = [
    "EmailPw",
    "Token",
]
