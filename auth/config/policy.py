from pydantic import BaseModel


class AuthPolicy(BaseModel):
    access_token_duration: int
    refresh_token_duration: int
    max_sessions: int
    private_key: bytes
