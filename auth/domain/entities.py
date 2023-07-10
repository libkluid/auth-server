from enum import Enum

from pydantic import BaseModel


class EmailPw(BaseModel):
    email: str
    password: str


class SignUp(BaseModel):
    uid: str
    email: str
    hash: str
    salt: str


class TokenType(str, Enum):
    ACCESS = "access-token"
    REFRESH = "refresh-token"


class AccessTokenPayload(BaseModel):
    sub: str
    ssn: str
    iat: int
    exp: int
    tty: TokenType = TokenType.ACCESS


class RefreshTokenPayload(BaseModel):
    sub: str
    ssn: str
    iat: int
    exp: int
    tty: TokenType = TokenType.REFRESH


class Token(BaseModel):
    access_token: str
    refresh_token: str


class AccessType(str, Enum):
    SIGNUP = "signup"
    SIGNIN = "signin"
