from datetime import datetime
from typing import Any, ClassVar, Generic, TypeVar

from pydantic import BaseModel

from auth.domain.entities import Token, TokenType

DataT = TypeVar("DataT")


class Response(BaseModel, Generic[DataT]):
    ok: bool
    error: None | str
    data: None | DataT

    class Config:
        json_encoders: ClassVar[dict[Any, Any]] = {
            datetime: lambda v: int(1000 * v.timestamp()),
        }


class Index(BaseModel):
    message: str


class User(BaseModel):
    uid: str
    created_at: datetime
    last_access: datetime


class Verify(BaseModel):
    sub: str
    ssn: str
    iat: int
    exp: int
    tty: TokenType


__all__ = [
    "Response",
    "Index",
    "Token",
    "User",
]
