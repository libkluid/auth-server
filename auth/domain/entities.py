from pydantic import BaseModel


class EmailPw(BaseModel):
    email: str
    password: str


class SignUp(BaseModel):
    uid: str
    email: str
    hash: str
    salt: str


class Token(BaseModel):
    access_token: str
    refresh_token: str
